# Dovecot Role

Installs and configures Dovecot 2.4 IMAP/LMTP server with Sieve support.

## Requirements

- **Debian 13 (Trixie) or newer** - Dovecot 2.4 has breaking changes incompatible with older versions
- MySQL database with ViMbAdmin schema (or compatible)
- Postfix for SMTP integration

## Features

- IMAP and LMTP protocols
- Sieve mail filtering with ManageSieve
- MySQL authentication (optimized for ViMbAdmin)
- Shared mailboxes with ACL support
- Quota management with Postfix policy service
- SSL/TLS encryption

## ViMbAdmin Integration

This role is optimized for use with [ViMbAdmin](https://www.vimbadmin.net/) as the mail
account management interface. The SQL queries are tailored to the vimbadmin database schema.

If you use a different mail management system, you may need to adjust the SQL queries
in `templates/dovecot.conf.j2`.

## Role Variables

### Required Variables (set in host_vars)

```yaml
dovecot_db_password: 'your_database_password'
dovecot_ssl_cert_file: /etc/letsencrypt/live/mail.example.com/fullchain.pem
dovecot_ssl_key_file: /etc/letsencrypt/live/mail.example.com/privkey.pem
```

### Optional Variables

```yaml
# Database configuration
dovecot_db_name: vimbadmin
dovecot_db_user: vimbadmin
dovecot_db_host: 127.0.0.1

# Mail storage
dovecot_vmail_user: vmail
dovecot_vmail_group: vmail
dovecot_vmail_home: '/var/vmail'

# Postmaster address for bounce messages
dovecot_postmaster_address: 'postmaster@example.com'

# Password scheme
dovecot_default_pass_scheme: SHA512-CRYPT
```

## Dependencies

- `alphanodes.setup.common`

## Example Playbook

```yaml
- hosts: mailservers
  roles:
    - role: alphanodes.setup.dovecot
      vars:
        dovecot_db_password: "{{ vault_dovecot_db_password }}"
        dovecot_ssl_cert_file: /etc/letsencrypt/live/{{ ansible_host }}/fullchain.pem
        dovecot_ssl_key_file: /etc/letsencrypt/live/{{ ansible_host }}/privkey.pem
        dovecot_postmaster_address: postmaster@example.com
```

## License

MIT
