# Ansible Role: memcached

An Ansible Role that installs [Memcached](https://memcached.org/) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.memcached
```
