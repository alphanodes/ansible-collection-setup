# Ansible Role: Rspamd

[![alphanodes.setup.rspamd](https://github.com/alphanodes/ansible.setup/actions/workflows/rspamd.yml/badge.svg)](https://github.com/alphanodes/ansible.setup/actions/workflows/rspamd.yml)

Install and configure Rspamd spam filtering system with DKIM signing support.

## Description

This role installs and configures Rspamd, a modern spam filtering system with built-in DKIM signing, ARC support, and Redis integration for learning and statistics.

**Key Features:**

- Rspamd installation from official repositories
- Automatic DKIM key generation and configuration
- Redis integration for statistics and learning
- Web UI with password protection
- Nginx vhost support (optional)
- Whitelist/blacklist management
- Milter protocol support for Postfix integration

## Requirements

- Ansible 2.18+
- Debian 11+ or Ubuntu 22.04+
- Redis server (automatically installed as dependency)

## Role Variables

### Required Variables

```yaml
# Controller password (generate with: rspamadm pw)
rspamd_worker_controller_password: '$2$...'
```

### DKIM Configuration

**Option 1: Automatic DKIM setup (recommended)**

```yaml
# Rspamd will automatically setup DKIM using alphanodes.setup.dkim role
rspamd_dkim_domains:
  - domain: example.com
    selector: mail
    key_size: 2048
  - domain: example.org
    selector: default
    key_size: 2048
```

**Option 2: Use existing DKIM keys**

```yaml
# Point to pre-existing DKIM keys
rspamd_dkim_key: /var/lib/dkim/example.com/mail.key
rspamd_dkim_selector: mail
```

### Optional Variables

```yaml
# Enable rspamd service
rspamd_enable_service: true

# Log level (error, warning, notice, info, debug)
rspamd_log_level: warning

# Redis configuration
rspamd_redis_servers: "127.0.0.1"
rspamd_redis_db: 1

# Web UI configuration
rspamd_vhost_server: rspamd.local
rspamd_web_user: rspamd
rspamd_web_password: ''  # Empty = no basic auth

# Whitelist/Blacklist
rspamd_whitelist_ip: []
rspamd_whitelist_from: []
rspamd_blacklist_ip: []
rspamd_blacklist_from: []
```

## Dependencies

This role automatically includes:

- `alphanodes.setup.common` - Common setup tasks
- `alphanodes.setup.redis_server` - Redis server for statistics
- `alphanodes.setup.dkim` - DKIM key management (when `rspamd_dkim_domains` is defined)

## Example Playbook

### Basic Setup with DKIM

```yaml
- hosts: mail_servers
  roles:
    - role: alphanodes.setup.rspamd
      vars:
        rspamd_worker_controller_password: '$2$...'
        rspamd_dkim_domains:
          - domain: example.com
            selector: mail
            key_size: 2048
```

### Advanced Setup

```yaml
- hosts: mail_servers
  roles:
    - role: alphanodes.setup.rspamd
      vars:
        rspamd_worker_controller_password: '$2$...'
        rspamd_dkim_domains:
          - domain: example.com
            selector: mail
            key_size: 2048
        rspamd_log_level: info
        rspamd_whitelist_ip:
          - 192.168.1.0/24
          - 10.0.0.0/8
        rspamd_vhost_server: spam.example.com
        rspamd_web_user: admin
        rspamd_web_password: 'secure_password_hash'
```

### Migration from existing DKIM

```yaml
- hosts: mail_servers
  roles:
    - role: alphanodes.setup.rspamd
      vars:
        rspamd_worker_controller_password: '$2$...'
        rspamd_dkim_key: /var/lib/dkim/example.com/mail.key
        rspamd_dkim_selector: mail
```

## Postfix Integration

Add to Postfix `/etc/postfix/main.cf`:

```text
# Rspamd milter
smtpd_milters = inet:localhost:11332
non_smtpd_milters = inet:localhost:11332
milter_protocol = 6
milter_mail_macros = i {mail_addr} {client_addr} {client_name} {auth_authen}
milter_default_action = accept
```

## Web UI Access

Access the Rspamd web UI at:

- Without vhost: `http://yourserver:11333`
- With vhost: `https://rspamd.yourdomain.com/` (requires nginx setup)

Login with the password you generated with `rspamadm pw`.

## Generate Controller Password

```bash
# On the target server
rspamadm pw
# Enter your password when prompted
# Copy the hash to rspamd_worker_controller_password
```

## DNS Configuration

After installation with DKIM enabled, add the DNS TXT records:

```bash
# View DKIM public key
cat /var/lib/dkim/example.com/mail.txt

# Verify DNS propagation
dig +short TXT mail._domainkey.example.com
```

## Testing

Run Molecule tests:

```bash
MOLECULE_DISTRO=debian12 molecule test -s rspamd
```

## Service Ports

- **11332**: Milter protocol (Postfix integration)
- **11333**: Web UI and HTTP API
- **11334**: Normal worker (scanning)

## Troubleshooting

### Check Rspamd status

```bash
systemctl status rspamd
rspamc stat
```

### Test DKIM signing

```bash
# Check DKIM configuration
rspamadm dkim_keygen -s mail -d example.com

# Test with email
rspamc --ip 192.168.1.1 < test_email.eml
```

### View logs

```bash
journalctl -u rspamd -f
```

## License

Apache License 2.0

## Author

AlphaNodes
