# Ansible Role: barman

Run barman backups and install/setup barman on Debian and Ubuntu servers.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

## Dependencies

- alphanodes.setup.postgresql_client

## Example Playbook

```yaml
    - hosts: your-barman-server
      vars:
        barman_postgresql_password: yoursecretpassword
      roles:
        - alphanodes.barman
```
