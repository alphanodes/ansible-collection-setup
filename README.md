# Ansible Collection - alphanodes.setup

## Description

This collection provides setup for:

- Linux operating systems:
  - Debian 11/12/13
  - Ubuntu 20.04/22.04

All provided roles do not use docker as container system.

## Minimum required Ansible-version

- Ansible >= 2.15.0

## Included content

- [alphanodes.setup.ansible_node](roles/ansible_node/)
- [alphanodes.setup.apt](roles/apt/)
- [alphanodes.setup.barman](roles/barman/) [![barman](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/barman.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/barman.yml)
- [alphanodes.setup.btrbk](roles/btrbk/)
- [alphanodes.setup.cifs_mount](roles/cifs_mount/)
- [alphanodes.setup.common](roles/common/)
- [alphanodes.setup.dendrite](roles/dendrite/) [![dendrite](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/dendrite.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/dendrite.yml)
- [alphanodes.setup.diagnostic](roles/diagnostic/) [![diagnostic](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/diagnostic.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/diagnostic.yml)
- [alphanodes.setup.drupal](roles/drupal/)
- [alphanodes.setup.drush](roles/drush/)
- [alphanodes.setup.element_web](roles/element_web/)
- [alphanodes.setup.ethercalc](roles/ethercalc/) [![ethercalc](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/ethercalc.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/ethercalc.yml)
- [alphanodes.setup.fail2ban](roles/fail2ban/)
- [alphanodes.setup.git](roles/git/)
- [alphanodes.setup.git_config](roles/git_config/)
- [alphanodes.setup.gitlab](roles/gitlab/)
- [alphanodes.setup.gitlab_omnibus](roles/gitlab_omnibus/)
- [alphanodes.setup.goaccess](roles/goaccess/)
- [alphanodes.setup.golang](roles/golang/) [![golang](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/golang.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/golang.yml)
- [alphanodes.setup.grafana](roles/grafana/)
- [alphanodes.setup.hedgedoc](roles/hedgedoc/)
- [alphanodes.setup.java](roles/java/)
- [alphanodes.setup.jekyll](roles/jekyll/)
- [alphanodes.setup.loki](roles/loki/)
- [alphanodes.setup.matomo](roles/matomo/)
- [alphanodes.setup.memcached](roles/memcached/) [![memcached](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/memcached.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/memcached.yml)
- [alphanodes.setup.mongodb](roles/mongodb/) [![mongodb](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mongodb.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mongodb.yml)
- [alphanodes.setup.mysql](roles/mysql/) [![mysql](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mysql.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mysql.yml)
- [alphanodes.setup.mysql_client](roles/mysql_client/) [![mysql_client](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mysql_client.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mysql_client.yml)
- [alphanodes.setup.netfilter](roles/netfilter/)
- [alphanodes.setup.nextcloud](roles/nextcloud/)
- [alphanodes.setup.nfs](roles/nfs/)
- [alphanodes.setup.nginx](roles/nginx/)
- [alphanodes.setup.nginx_mono](roles/nginx_mono/) [![nginx_mono](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/nginx_mono.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/nginx_mono.yml)
- [alphanodes.setup.nodejs](roles/nodejs/) [![nodejs](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/nodejs.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/nodejs.yml)
- [alphanodes.setup.php_cli](roles/php_cli/)
- [alphanodes.setup.php_fpm](roles/php_fpm/)
- [alphanodes.setup.phpmyadmin](roles/phpmyadmin/)
- [alphanodes.setup.postfix](roles/postfix/)
- [alphanodes.setup.postgresql](roles/postgresql/) [![postgresql](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/postgresql.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/postgresql.yml)
- [alphanodes.setup.postgresql_client](roles/postgresql_client/) [![postgresql_client](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/postgresql_client.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/postgresql_client.yml)
- [alphanodes.setup.python](roles/python/) [![python](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/python.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/python.yml)
- [alphanodes.setup.redis_server](roles/redis_server/)
- [alphanodes.setup.redmine](roles/redmine/)
- [alphanodes.setup.rocketchat](roles/rocketchat/) [![rocketchat](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/rocketchat.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/rocketchat.yml)
- [alphanodes.setup.rsync](roles/rsync/)
- [alphanodes.setup.rvm](roles/rvm/)
- [alphanodes.setup.sphinx](roles/sphinx/)
- [alphanodes.setup.ssh](roles/ssh/) [![ssh](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/ssh.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/ssh.yml)
- [alphanodes.setup.ssl](roles/ssl/)
- [alphanodes.setup.sudo](roles/sudo/)
- [alphanodes.setup.svn](roles/svn/) [![svn](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/svn.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/svn.yml)
- [alphanodes.setup.swapfile](roles/swapfile/)
- [alphanodes.setup.systemd_timer](roles/systemd_timer/) [![systemd_timer](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/systemd_timer.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/systemd_timer.yml)
- [alphanodes.setup.unbound](roles/unbound/)
- [alphanodes.setup.wordpress](roles/wordpress/)
- [alphanodes.setup.zsh](roles/zsh/)

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
