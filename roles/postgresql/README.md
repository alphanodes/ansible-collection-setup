# Ansible Role: postgresql

An Ansible Role that installs PostgreSQL server on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        postgresql_version: '18'
        postgresql_with_postgis: true

      roles:
        - alphanodes.setup.postgresql
```
