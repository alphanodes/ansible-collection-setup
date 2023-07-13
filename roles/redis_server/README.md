# Ansible Role: redis_server

An Ansible Role that installs [redis](https://redis.io/) on Debian and Ubuntu.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.redis_server
```
