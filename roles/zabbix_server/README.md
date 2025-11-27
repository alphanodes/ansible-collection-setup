# Zabbix Server

Installs and configures Zabbix Server with PostgreSQL backend and nginx web frontend.

## Requirements

- PostgreSQL database server
- PHP-FPM for web interface
- nginx (via nginx_mono role)

## Role Variables

See `defaults/main.yml` for available variables.

## Dependencies

- alphanodes.setup.common
- alphanodes.setup.zabbix_agent
- alphanodes.setup.postgresql
- alphanodes.setup.php_fpm

## Example Playbook

```yaml
- hosts: monitoring
  roles:
    - role: alphanodes.setup.zabbix_server
      vars:
        zabbix_server_vhost: monitor.example.com
        zabbix_server_vhost_ssl_cert: monitor
```

## License

Apache-2.0
