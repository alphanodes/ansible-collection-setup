# Ansible Collection - alphanodes.setup

## Description

This collection provides setup for:

- Linux operating systems:
  - Debian 10/11/12
  - Ubuntu 20.04/22.04

All provided roles do not use docker as container system.

## Minimum required Ansible-version

- Ansible >= 2.15.0

## Included content

- [alphanodes.setup.ansible_node](roles/ansible_node/)
- [alphanodes.setup.apt](roles/apt/)
- [alphanodes.setup.barman](roles/barman/)
- [alphanodes.setup.cifs_mount](roles/cifs_mount/)
- [alphanodes.setup.drupal](roles/drupal/)
- [alphanodes.setup.drush](roles/drush/)
- [alphanodes.setup.ethercalc](roles/ethercalc/)
- [alphanodes.setup.fail2ban](roles/fail2ban/)
- [alphanodes.setup.git](roles/git/)
- [alphanodes.setup.git_config](roles/git_config/)
- [alphanodes.setup.gitlab](roles/gitlab/)
- [alphanodes.setup.glances](roles/glances/)
- [alphanodes.setup.goaccess](roles/goaccess/)
- [alphanodes.setup.hedgedoc](roles/hedgedoc/)
- [alphanodes.setup.java](roles/java/)
- [alphanodes.setup.jekyll](roles/jekyll/)
- [alphanodes.setup.matomo](roles/matomo/)
- [alphanodes.setup.memcached](roles/memcached/)
- [alphanodes.setup.mongodb](roles/mongodb/)
- [alphanodes.setup.mysql](roles/mysql/)
- [alphanodes.setup.mysql_client](roles/mysql_client/)
- [alphanodes.setup.netfilter](roles/netfilter/)
- [alphanodes.setup.nextcloud](roles/nextcloud/)
- [alphanodes.setup.nfs](roles/nfs/)
- [alphanodes.setup.nginx](roles/nginx/)
- [alphanodes.setup.nodejs](roles/nodejs/)
- [alphanodes.setup.php_cli](roles/php_cli/)
- [alphanodes.setup.php_fpm](roles/php_fpm/)
- [alphanodes.setup.phpmyadmin](roles/phpmyadmin/)
- [alphanodes.setup.python](roles/python/)
- [alphanodes.setup.postfix](roles/postfix/)
- [alphanodes.setup.postgresql](roles/postgresql/)
- [alphanodes.setup.postgresql_client](roles/postgresql_client/)
- [alphanodes.setup.redis_server](roles/redis_server/)
- [alphanodes.setup.redmine](roles/redmine/)
- [alphanodes.setup.rocketchat](roles/rocketchat/)
- [alphanodes.setup.rsync](roles/rsync/)
- [alphanodes.setup.sphinx](roles/sphinx/)
- [alphanodes.setup.ssh](roles/ssh/)
- [alphanodes.setup.ssl](roles/ssl/)
- [alphanodes.setup.sudo](roles/sudo/)
- [alphanodes.setup.svn](roles/svn/)
- [alphanodes.setup.swapfile](roles/swapfile/)
- [alphanodes.setup.systemd_timer](roles/systemd_timer/)
- [alphanodes.setup.unbound](roles/unbound/)
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
