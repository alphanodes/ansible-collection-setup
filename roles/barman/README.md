# Ansible Role: barman

Run barman backups and install/setup barman on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        barman_postgresql_password: yoursecretpassword

      roles:
        - alphanodes.barman
```
