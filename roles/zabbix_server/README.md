# Ansible Role: zabbix_server

An Ansible Role that installs [Zabbix](https://www.zabbix.com/) Server with PostgreSQL backend and nginx web frontend on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        zabbix_server_vhost: monitor.example.com

      roles:
        - alphanodes.setup.zabbix_server
```
