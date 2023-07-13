# Ansible Role: PostgreSQL-Client

Installs PostgreSQL client on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        postgresql_client_use_repo: true

      roles:
        - alphanodes.setup.postgresql_client
```
