# Ansible Role: Radicale

Installs and configures [Radicale](https://radicale.org/) CalDAV/CardDAV server with nginx reverse proxy.

## Requirements

- Debian 12/13 or Ubuntu 24.04
- nginx_mono role for vhost configuration

## Role Variables

See `defaults/main.yml` for all available variables.

### Key Variables

```yaml
# Server configuration
radicale_vhost_server: radicale.example.com
radicale_server_host: 127.0.0.1:5232

# Authentication (http_x_remote_user uses nginx basic auth)
radicale_auth_type: http_x_remote_user
radicale_users:
  - user: admin
    password: secret

# Rights configuration
radicale_rights:
  - name: admin
    user: admin
    collection: ''
    permissions: RW
  - name: principal
    user: '.+'
    collection: '{user}'
    permissions: RW
```

## Dependencies

- alphanodes.setup.common
- alphanodes.setup.python
- alphanodes.setup.nginx_mono
- alphanodes.setup.systemd_timer

## Example Playbook

```yaml
- hosts: calendar
  roles:
    - role: alphanodes.setup.radicale
      vars:
        radicale_vhost_server: calendar.example.com
        radicale_vhost_letsencrypt: true
        radicale_users:
          - user: admin
            password: supersecret
```

## License

MIT
