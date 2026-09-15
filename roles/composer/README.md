# Ansible Role: composer

An Ansible Role that installs [Composer](https://getcomposer.org/) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.php_cli
        - alphanodes.setup.composer
```
