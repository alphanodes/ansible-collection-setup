# Ansible Role: PostgreSQL

Installs PostgreSQL server on Debian and Ubuntu servers.

## Example Playbook

```yaml
    - hosts: db-server
      vars:
        postgresql_version: '15'
        postgresql_with_postgis: true
      roles:
        - alphanodes.setup.postgresql
```
