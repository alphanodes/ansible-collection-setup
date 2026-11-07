"""Exercise credential handling across YAML, shell and Ruby template boundaries."""
import base64
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import yaml
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar

try:
    from ansible.template import trust_as_template
except ImportError:
    def trust_as_template(value):
        return value


TEMPLATES = Path(__file__).resolve().parents[3] / 'roles' / 'zammad' / 'templates'


def render(name, variables):
    variables = dict(variables, managed_by_ansible='Managed by Ansible')
    return Templar(loader=DataLoader(), variables=variables).template(
        trust_as_template((TEMPLATES / name).read_text())
    )


class TemplateTest(unittest.TestCase):
    @unittest.skipUnless(shutil.which('ruby'), 'Ruby is required to exercise Rails ERB and YAML processing')
    def test_database_password_remains_a_literal_yaml_string(self):
        password = (
            "quote'\" backslash\\ newline\ncolon: #{raise 'interpolation'} "
            "<%= raise 'ERB interpolation' %> <% raise 'ERB execution' %> "
            "<% invalid ruby syntax ! %> \\u003c äöüß"
        )
        content = render('database.yml.j2', {
            'zammad_db_name': 'helpdesk', 'zammad_db_user': 'helpdesk',
            'zammad_db_password': password, 'zammad_db_host': '127.0.0.1',
            'zammad_db_port': 5543, 'zammad_db_pool': 50,
        })
        settings = yaml.safe_load(content)['production']
        self.assertEqual(settings['password'], password)
        self.assertEqual(settings['port'], 5543)
        # Rails processes database.yml with ERB before loading the resulting YAML.
        result = subprocess.run(
            ['ruby', '-rerb', '-ryaml', '-rjson', '-e',
             'puts JSON.generate(YAML.safe_load(ERB.new(STDIN.read).result))'],
            input=content, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['production'], settings)

    def test_shell_environment_preserves_literal_metacharacters(self):
        url = 'redis://:password-$USER-$(false)-\'"@127.0.0.1:6379/5'
        content = render('environment.j2', {
            'zammad_http_port': 3100, 'zammad_websocket_port': 6142,
            'zammad_web_concurrency': 1, 'zammad_redis_url': url,
        })
        with tempfile.TemporaryDirectory() as work:
            path = Path(work) / 'environment'
            path.write_text(content)
            result = subprocess.check_output(
                ['/bin/sh', '-c', '. "$1"; printf %s "$REDIS_URL"', 'test', str(path)],
                text=True,
            )
        self.assertEqual(result, url)

    @unittest.skipUnless(shutil.which('ruby'), 'Ruby is required to execute the generated settings script')
    def test_disabled_search_never_connects_to_index_backend(self):
        content = render('configure.rb.j2', {
            'zammad_with_elasticsearch': False, 'zammad_settings': {},
            'zammad_vhost_server': 'support.example.com', 'nginx_with_ssl': True,
            'zammad_elasticsearch_url': 'http://unused.invalid:9200',
            'zammad_elasticsearch_user': '', 'zammad_elasticsearch_password': '',
            'zammad_elasticsearch_index': 'helpdesk',
        })
        stubs = """
class User
  def self.exists?; true; end
end
class Setting
  def self.get(name); (@values ||= {})[name]; end
  def self.set(name, value); (@values ||= {})[name] = value; end
end
class SearchIndexBackend
  def self.index_exists?(name); raise 'Search backend must remain unused'; end
end
"""
        with tempfile.TemporaryDirectory() as work:
            path = Path(work) / 'configure.rb'
            path.write_text(stubs + content + "raise 'Search URL still enabled' unless Setting.get('es_url') == ''\n")
            result = subprocess.run(['ruby', str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('ZAMMAD_REINDEX', result.stdout)

    @unittest.skipUnless(shutil.which('ruby'), 'Ruby is required to execute the generated settings script')
    def test_ruby_settings_do_not_interpolate_credentials(self):
        password = '#{raise "credential interpolation"}'
        content = render('configure.rb.j2', {
            'zammad_with_elasticsearch': True,
            'zammad_settings': {}, 'zammad_vhost_server': 'support.example.com',
            'nginx_with_ssl': True, 'zammad_elasticsearch_url': 'http://127.0.0.1:9200',
            'zammad_elasticsearch_user': '', 'zammad_elasticsearch_password': password,
            'zammad_elasticsearch_index': 'helpdesk',
        })
        stubs = '''
class User
  def self.exists?; true; end
end
class Setting
  def self.get(name); (@values ||= {})[name]; end
  def self.set(name, value); (@values ||= {})[name] = value; end
end
class SearchIndexBackend
  def self.index_exists?(name); true; end
end
'''
        expected = base64.b64encode(json.dumps(password).encode()).decode()
        assertion = (
            "raise 'Credential changed' unless Setting.get('es_password') == "
            "JSON.parse(Base64.strict_decode64('" + expected + "'))\n"
        )
        with tempfile.TemporaryDirectory() as work:
            path = Path(work) / 'configure.rb'
            path.write_text(stubs + content + assertion)
            result = subprocess.run(['ruby', str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
