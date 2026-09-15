# Ansible Role: zabbix_agent

An Ansible Role that installs [Zabbix](https://www.zabbix.com/) Agent 2 with custom monitoring scripts on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        zabbix_server_vhost: monitor.example.com

      roles:
        - alphanodes.setup.zabbix_agent
```
