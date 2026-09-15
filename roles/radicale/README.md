# Ansible Role: radicale

An Ansible Role that installs the [Radicale](https://radicale.org/) CalDAV/CardDAV server behind nginx on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        radicale_vhost_server: calendar.example.com
        radicale_users:
          - user: admin
            password: secret

      roles:
        - alphanodes.setup.radicale
```
