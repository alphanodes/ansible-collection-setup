"""Exercise backup publication, retention and recovery without system services."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[3] / 'roles/zammad/files/zammad-backup.py'
SPEC = importlib.util.spec_from_file_location('zammad_backup', SCRIPT)
backup = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(backup)


class BackupTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.destination = self.root / 'backups'
        self.destination.mkdir()
        self.config_dir = self.root / 'opt/zammad/config'
        self.storage_dir = self.root / 'opt/zammad/storage'
        self.settings_dir = self.root / 'etc/zammad'
        for directory in (self.config_dir, self.storage_dir, self.settings_dir):
            directory.mkdir(parents=True)
        (self.config_dir / 'database.yml').write_text('production: {}\n')
        (self.storage_dir / 'attachment.txt').write_text('ticket attachment')
        self.config_file = self.root / 'etc/zammad-backup.json'
        self.config_file.write_text(json.dumps({
            'directory': str(self.destination), 'host': '127.0.0.1',
            'port': 5432, 'database': 'zammad', 'user': 'zammad',
            'password': 'test-password', 'pg_dump': '/test/pg_dump',
            'hold_days': 7,
        }))
        self.add_patch('CONFIG_FILE', self.config_file)
        self.add_patch('LOCK_FILE', self.root / 'backup.lock')
        self.add_patch('BACKUP_PATHS', tuple(map(str, (
            self.config_dir, self.storage_dir, self.settings_dir, self.config_file,
        ))))
        # The production umask must not change the test runner's process state.
        self.add_patch('os.umask')
        self.running = True
        self.run = self.add_patch('subprocess.run', side_effect=self.run_command)
        self.add_patch('subprocess.check_output', return_value='7.2.2-test')

    def add_patch(self, name, *args, **kwargs):
        # importlib modules need not be registered in sys.modules; patch nested
        # attributes on the imported objects directly instead of resolving names.
        if '.' in name:
            owner, attribute = name.split('.')
            patcher = patch.object(getattr(backup, owner), attribute, *args, **kwargs)
        else:
            patcher = patch.object(backup, name, *args, **kwargs)
        mocked = patcher.start()
        self.addCleanup(patcher.stop)
        return mocked

    def run_command(self, argv, **kwargs):
        if argv[:2] == ['systemctl', 'is-active']:
            return SimpleNamespace(returncode=0 if self.running else 3)
        if argv[0] == '/test/pg_dump':
            self.assertTrue(kwargs['check'])
            self.assertEqual(kwargs['env']['PGDATABASE'], 'zammad')
            self.assertEqual(kwargs['env']['PGPASSWORD'], 'test-password')
            Path(argv[argv.index('--file') + 1]).write_bytes(b'PGDMP-test-data')
        return SimpleNamespace(returncode=0)

    def execute(self):
        with contextlib.redirect_stdout(io.StringIO()):
            backup.main()

    def expired_backup(self):
        old = self.destination / 'zammad-old.tar'
        old.write_bytes(b'existing backup')
        expired = time.time() - 30 * 86400
        os.utime(old, (expired, expired))
        return old

    def test_dump_failure_restarts_application_without_publication_or_retention(self):
        old = self.expired_backup()

        def fail_dump(argv, **kwargs):
            if argv[0] == '/test/pg_dump':
                raise subprocess.CalledProcessError(1, argv, stderr='dump failed')
            return self.run_command(argv, **kwargs)

        self.run.side_effect = fail_dump
        with self.assertRaises(subprocess.CalledProcessError):
            self.execute()

        self.run.assert_any_call(['systemctl', 'stop', 'zammad'], check=True)
        self.assertEqual(self.run.call_args.args[0], ['systemctl', 'start', 'zammad'])
        self.assertEqual(list(self.destination.iterdir()), [old])
        self.assertEqual(old.read_bytes(), b'existing backup')

    def test_success_publishes_dump_files_and_version_then_expires_old_backup(self):
        old = self.expired_backup()
        self.execute()

        self.assertFalse(old.exists())
        published = list(self.destination.glob('zammad-*.tar'))
        self.assertEqual(len(published), 1)
        self.assertEqual(list(self.destination.iterdir()), published)
        with tarfile.open(published[0]) as archive:
            self.assertEqual(set(archive.getnames()), {
                'database.dump', 'files.tar.gz', 'version.txt',
            })
            self.assertEqual(archive.extractfile('database.dump').read(), b'PGDMP-test-data')
            self.assertEqual(archive.extractfile('version.txt').read(), b'7.2.2-test\n')
            files = archive.extractfile('files.tar.gz').read()
        with tarfile.open(fileobj=io.BytesIO(files), mode='r:gz') as archive:
            attachment = str(self.storage_dir / 'attachment.txt').lstrip('/')
            self.assertEqual(archive.extractfile(attachment).read(), b'ticket attachment')
            self.assertIn(str(self.config_file).lstrip('/'), archive.getnames())
        self.assertEqual(self.run.call_args.args[0], ['systemctl', 'start', 'zammad'])

    def test_stopped_application_is_not_started_by_backup(self):
        self.running = False
        self.execute()
        service_actions = [call.args[0] for call in self.run.call_args_list if call.args[0][0] == 'systemctl']
        self.assertEqual(service_actions, [['systemctl', 'is-active', '--quiet', 'zammad']])

    def test_symlink_storage_is_rejected_before_stopping_application(self):
        external = self.root / 'external-storage'
        self.storage_dir.rename(external)
        self.storage_dir.symlink_to(external, target_is_directory=True)
        with self.assertRaisesRegex(RuntimeError, 'not a symlink'):
            self.execute()
        self.run.assert_not_called()
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_archive_failure_restarts_application_and_keeps_previous_backup(self):
        old = self.expired_backup()
        with patch.object(backup.tarfile, 'open', side_effect=OSError('archive failed')):
            with self.assertRaisesRegex(OSError, 'archive failed'):
                self.execute()
        self.assertEqual(self.run.call_args.args[0], ['systemctl', 'start', 'zammad'])
        self.assertEqual(list(self.destination.iterdir()), [old])


if __name__ == '__main__':
    unittest.main()
