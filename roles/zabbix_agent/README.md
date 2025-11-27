# Role: zabbix_agent

Installs and configures Zabbix Agent 2 with custom monitoring scripts.

## Supported platforms

- Debian 12/13
- Ubuntu 24.04

## Dependencies

- alphanodes.setup.common
- alphanodes.setup.rsync

## Variables

See `defaults/main.yml` for all configurable options. Key variables:

- `zabbix_server_vhost` - Zabbix server hostname
- `zabbix_version` - Zabbix version (default: 7.4)
- `zabbix_agent_server_api` - Enable Zabbix API integration
- `zabbix_host_groups` - Host groups for Zabbix API
- `zabbix_link_templates` - Templates to link via API
