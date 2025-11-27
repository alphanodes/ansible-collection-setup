# Ansible Collection - alphanodes.setup

[![Linter](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/linter.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/linter.yml)

## Description

This collection provides setup for:

- Linux operating systems:
  - Debian 12/13
  - Ubuntu 24.04

All provided roles do not use docker as container system.

## Minimum required Ansible-version

- Ansible >= 2.18.0

## Included content

- [alphanodes.setup.alloy](roles/alloy/) [![alloy](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/alloy.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/alloy.yml)
- [alphanodes.setup.ansible_node](roles/ansible_node/) [![ansible_node](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/ansible_node.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/ansible_node.yml)
- [alphanodes.setup.apt](roles/apt/) [![apt](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/apt.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/apt.yml)
- [alphanodes.setup.barman](roles/barman/) [![barman](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/barman.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/barman.yml)
- [alphanodes.setup.btrbk](roles/btrbk/) [![btrbk](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/btrbk.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/btrbk.yml)
- [alphanodes.setup.certbot](roles/certbot/) [![certbot](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/certbot.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/certbot.yml)
- [alphanodes.setup.cifs_mount](roles/cifs_mount/) [![cifs_mount](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/cifs_mount.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/cifs_mount.yml)
- [alphanodes.setup.clamav](roles/clamav/) [![clamav](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/clamav.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/clamav.yml)
- [alphanodes.setup.common](roles/common/) [![common](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/common.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/common.yml)
- [alphanodes.setup.composer](roles/composer/) [![composer](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/composer.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/composer.yml)
- [alphanodes.setup.dendrite](roles/dendrite/) [![dendrite](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/dendrite.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/dendrite.yml)
- [alphanodes.setup.diagnostic](roles/diagnostic/) [![diagnostic](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/diagnostic.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/diagnostic.yml)
- [alphanodes.setup.dkim](roles/dkim/) [![dkim](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/dkim.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/dkim.yml)
- [alphanodes.setup.drupal](roles/drupal/) [![drupal](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/drupal.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/drupal.yml)
- [alphanodes.setup.drush](roles/drush/) [![drush](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/drush.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/drush.yml)
- [alphanodes.setup.element_web](roles/element_web/) [![element_web](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/element_web.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/element_web.yml)
- [alphanodes.setup.ethercalc](roles/ethercalc/) [![ethercalc](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/ethercalc.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/ethercalc.yml)
- [alphanodes.setup.fail2ban](roles/fail2ban/) [![fail2ban](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/fail2ban.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/fail2ban.yml)
- [alphanodes.setup.git](roles/git/) [![git](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/git.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/git.yml)
- [alphanodes.setup.git_config](roles/git_config/) [![git_config](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/git_config.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/git_config.yml)
- [alphanodes.setup.gitlab](roles/gitlab/) [![gitlab](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/gitlab.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/gitlab.yml)
- [alphanodes.setup.gitlab_omnibus](roles/gitlab_omnibus/) [![gitlab_omnibus](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/gitlab_omnibus.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/gitlab_omnibus.yml)
- [alphanodes.setup.goaccess](roles/goaccess/) [![goaccess](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/goaccess.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/goaccess.yml)
- [alphanodes.setup.golang](roles/golang/) [![golang](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/golang.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/golang.yml)
- [alphanodes.setup.grafana](roles/grafana/) [![grafana](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/grafana.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/grafana.yml)
- [alphanodes.setup.hedgedoc](roles/hedgedoc/) [![hedgedoc](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/hedgedoc.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/hedgedoc.yml)
- [alphanodes.setup.java](roles/java/) [![java](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/java.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/java.yml)
- [alphanodes.setup.jekyll](roles/jekyll/) [![jekyll](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/jekyll.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/jekyll.yml)
- [alphanodes.setup.loki](roles/loki/) [![loki](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/loki.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/loki.yml)
- [alphanodes.setup.mailpit](roles/mailpit/) [![mailpit](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mailpit.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mailpit.yml)
- [alphanodes.setup.matomo](roles/matomo/) [![matomo](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/matomo.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/matomo.yml)
- [alphanodes.setup.memcached](roles/memcached/) [![memcached](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/memcached.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/memcached.yml)
- [alphanodes.setup.mongodb](roles/mongodb/) [![mongodb](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mongodb.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mongodb.yml)
- [alphanodes.setup.mysql](roles/mysql/) [![mysql](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mysql.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mysql.yml)
- [alphanodes.setup.mysql_client](roles/mysql_client/) [![mysql_client](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mysql_client.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mysql_client.yml)
- [alphanodes.setup.netfilter](roles/netfilter/) [![netfilter](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/netfilter.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/netfilter.yml)
- [alphanodes.setup.nextcloud](roles/nextcloud/) [![nextcloud](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/nextcloud.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/nextcloud.yml)
- [alphanodes.setup.nfs](roles/nfs/) [![nfs](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/nfs.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/nfs.yml)
- [alphanodes.setup.nginx](roles/nginx/) [![nginx](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/nginx.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/nginx.yml)
- [alphanodes.setup.nginx_mono](roles/nginx_mono/) [![nginx_mono](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/nginx_mono.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/nginx_mono.yml)
- [alphanodes.setup.nodejs](roles/nodejs/) [![nodejs](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/nodejs.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/nodejs.yml)
- [alphanodes.setup.php_cli](roles/php_cli/) [![php_cli](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/php_cli.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/php_cli.yml)
- [alphanodes.setup.php_fpm](roles/php_fpm/) [![php_fpm](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/php_fpm.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/php_fpm.yml)
- [alphanodes.setup.postfix](roles/postfix/) [![postfix](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/postfix.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/postfix.yml)
- [alphanodes.setup.postgresql](roles/postgresql/) [![postgresql](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/postgresql.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/postgresql.yml)
- [alphanodes.setup.postgresql_client](roles/postgresql_client/) [![postgresql_client](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/postgresql_client.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/postgresql_client.yml)
- [alphanodes.setup.python](roles/python/) [![python](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/python.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/python.yml)
- [alphanodes.setup.redis_server](roles/redis_server/) [![redis_server](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/redis_server.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/redis_server.yml)
- [alphanodes.setup.redmine](roles/redmine/) [![redmine](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/redmine.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/redmine.yml)
- [alphanodes.setup.rocketchat](roles/rocketchat/) [![rocketchat](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/rocketchat.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/rocketchat.yml)
- [alphanodes.setup.rspamd](roles/rspamd/) [![rspamd](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/rspamd.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/rspamd.yml)
- [alphanodes.setup.rsync](roles/rsync/) [![rsync](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/rsync.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/rsync.yml)
- [alphanodes.setup.ruby](roles/ruby/) [![ruby](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/ruby.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/ruby.yml)
- [alphanodes.setup.rvm](roles/rvm/) [![rvm](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/rvm.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/rvm.yml)
- [alphanodes.setup.sphinx](roles/sphinx/) [![sphinx](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/sphinx.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/sphinx.yml)
- [alphanodes.setup.ssh](roles/ssh/) [![ssh](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/ssh.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/ssh.yml)
- [alphanodes.setup.ssl](roles/ssl/) [![ssl](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/ssl.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/ssl.yml)
- [alphanodes.setup.sudo](roles/sudo/) [![sudo](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/sudo.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/sudo.yml)
- [alphanodes.setup.svn](roles/svn/) [![svn](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/svn.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/svn.yml)
- [alphanodes.setup.swapfile](roles/swapfile/) [![swapfile](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/swapfile.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/swapfile.yml)
- [alphanodes.setup.systemd_timer](roles/systemd_timer/) [![systemd_timer](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/systemd_timer.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/systemd_timer.yml)
- [alphanodes.setup.unbound](roles/unbound/) [![unbound](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/unbound.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/unbound.yml)
- [alphanodes.setup.zabbix_agent](roles/zabbix_agent/) [![zabbix_agent](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/zabbix_agent.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/zabbix_agent.yml)
- [alphanodes.setup.zsh](roles/zsh/) [![zsh](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/zsh.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/zsh.yml)

## Installation

Install the collection via ansible-galaxy:

`ansible-galaxy collection install alphanodes.setup`

or use latest (unreleased) version from git with:

`ansible-galaxy collection install git+https://github.com/alphanodes/ansible-collection-setup.git,main`

## Using this collection

Please refer to the examples in the readmes of the role.

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

See the [contributor guideline](CONTRIBUTING.md).

## Licensing

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
