# ViMbAdmin

Ansible role to install and configure ViMbAdmin (Virtual Mailbox Admin) for managing email domains, mailboxes, and aliases.

## Requirements

- Debian 12/13 (Bookworm/Trixie)

## Role Variables

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `vimbadmin_vhost_server` | `vimbadmin.local` | Server name for nginx vhost |
| `vimbadmin_vhost_letsencrypt` | `false` | Enable Let's Encrypt SSL |
| `vimbadmin_vhost_ssl_cert` | `''` | SSL certificate name (from ssl role) |
| `vimbadmin_securitysalt` | required | Security salt for session encryption |
| `vimbadmin_rememberme_salt` | required | Salt for remember me tokens |
| `vimbadmin_password_salt` | required | Salt for password hashing |
| `vimbadmin_identity_orgname` | `Example Organization` | Organization name |
| `vimbadmin_identity_email` | `support@example.com` | Support email address |

## Dependencies

- `alphanodes.setup.common`
- `alphanodes.setup.ssl`
- `alphanodes.setup.php_fpm`
- `alphanodes.setup.mysql`
- `alphanodes.setup.composer`
- `alphanodes.setup.memcached`
- `alphanodes.setup.postfix`
- `alphanodes.setup.dovecot`
- `alphanodes.setup.nginx_mono`

## Example Playbook

```yaml
- hosts: mail
  roles:
    - role: alphanodes.setup.vimbadmin
      vars:
        vimbadmin_vhost_server: mailconfig.example.com
        vimbadmin_vhost_ssl_cert: mailconfig
        vimbadmin_securitysalt: "{{ vault_vimbadmin_securitysalt }}"
        vimbadmin_rememberme_salt: "{{ vault_vimbadmin_rememberme_salt }}"
        vimbadmin_password_salt: "{{ vault_vimbadmin_password_salt }}"
        vimbadmin_identity_orgname: "My Company"
        vimbadmin_identity_email: "support@example.com"
```

## Security Note

The three salt variables (`vimbadmin_securitysalt`, `vimbadmin_rememberme_salt`, `vimbadmin_password_salt`) must be unique random strings and should be stored in Ansible Vault or another secure storage.

## License

MIT
