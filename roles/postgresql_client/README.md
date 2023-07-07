# Ansible Role: PostgreSQL-Client

Installs PostgreSQL client on Debian and Ubuntu servers.

## Example Playbook

```yaml
    - hosts: db-client
      vars:
        postgresql_client_use_repo: true
      roles:
        - alphanodes.setup.postgresql_client
```
