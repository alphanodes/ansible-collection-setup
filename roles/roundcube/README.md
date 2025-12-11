# Roundcube

Ansible role to install and configure Roundcube webmail.

## Requirements

- Debian 13 (Trixie)

## Role Variables

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `roundcube_vhost_server` | `roundcube.example.com` | Server name for nginx vhost |
| `roundcube_vhost_letsencrypt` | `false` | Enable Let's Encrypt SSL |
| `roundcube_vhost_ssl_cert` | `''` | SSL certificate name (from ssl role) |
| `roundcube_db_password` | required | Database password for Roundcube |
| `roundcube_git_install` | `false` | Install from Git instead of package |

## Dependencies

- `alphanodes.setup.common`
- `alphanodes.setup.ssl`
- `alphanodes.setup.php_fpm`
- `alphanodes.setup.mysql`
- `alphanodes.setup.nginx_mono`

## Example Playbook

```yaml
- hosts: mail
  roles:
    - role: alphanodes.setup.roundcube
      vars:
        roundcube_vhost_server: webmail.example.com
        roundcube_vhost_ssl_cert: webmail
        roundcube_db_password: "{{ vault_roundcube_db_password }}"
```

## Custom Files

Customer-specific files are loaded from playbook directory:

- `{{ playbook_dir }}/files/roundcube/logo/{{ inventory_hostname }}.png` - Custom logo
- `{{ playbook_dir }}/files/roundcube/config/{{ inventory_hostname }}/config.inc.php` - Custom config

## License

MIT
