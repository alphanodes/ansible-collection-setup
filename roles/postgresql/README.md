# Ansible Role: PostgreSQL

Installs PostgreSQL server on Debian and Ubuntu servers.

## Example Playbook

```yaml
    - hosts: all

      vars:
        postgresql_version: '18'
        postgresql_with_postgis: true

      roles:
        - alphanodes.setup.postgresql
```
