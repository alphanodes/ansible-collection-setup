# Ansible Role: dovecot

An Ansible Role that installs Dovecot 2.4 IMAP/LMTP server with Sieve support on Debian and Ubuntu servers.

## Requirements

- Debian 13 (Trixie) or newer, Dovecot 2.4 is incompatible with older configurations
- MySQL database with the ViMbAdmin schema, the SQL queries in `templates/dovecot.conf.j2` are tailored to it

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        dovecot_db_password: "{{ vault_dovecot_db_password }}"
        dovecot_ssl_cert_file: /etc/letsencrypt/live/mail.example.com/fullchain.pem
        dovecot_ssl_key_file: /etc/letsencrypt/live/mail.example.com/privkey.pem
        dovecot_postmaster_address: postmaster@example.com

      roles:
        - alphanodes.setup.dovecot
```

Without `dovecot_ssl_cert_file` and `dovecot_ssl_key_file` the role falls back to the snakeoil certificate, which is only suitable for tests.

## Server Side Spam Filing

A global Sieve script (`before.sieve`) runs before every personal filter and files marked mail into `dovecot_spam_mailbox`. The defaults are inert on purpose: rspamd emits no `X-Spam-Flag`, so the rule matches nothing and an existing installation keeps delivering to the inbox. To activate filing, enable the spam header in the rspamd role and point both sides at the same header:

```yaml
# rspamd host
rspamd_with_spam_header: true
rspamd_spam_header_name: X-Spam
rspamd_spam_header_value: 'Yes'

# dovecot host
dovecot_spam_header_name: X-Spam
dovecot_spam_header_value: 'Yes'
```

Mail scoring at or above `rspamd_action_add_header` then moves into the Junk folder, where nobody looks by default, so weigh the false positive risk before enabling it.
