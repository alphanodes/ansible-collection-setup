# Ansible Role: mailpit

[![alphanodes.setup.mailpit](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mailpit.yml/badge.svg)](https://github.com/alphanodes/ansible-collection-setup/actions/workflows/mailpit.yml)

Install and configure [Mailpit](https://github.com/axllent/mailpit) - a modern email testing tool for developers.

Mailpit is a multi-platform email testing tool that acts as both an SMTP server and provides a web interface to view and test emails.

## Features

- **SMTP Server**: Catches all outgoing emails on port 1025 (configurable)
- **Web UI**: Modern web interface to view emails on port 8025
- **HTML & Plain Text**: View emails in both HTML and plain text formats
- **Search & Filter**: Search through captured emails
- **Attachments**: View and download email attachments
- **REST API**: Programmatic access to emails
- **No Dependencies**: Single Go binary, no external dependencies

## Requirements

- Debian 12+ or Ubuntu 22.04+
- nginx_mono role for web interface (automatically included)

## Role Variables

### Basic Configuration

```yaml
# Mailpit version to install
# Can be a specific version (e.g. '1.20.0') or 'latest'
# When set to 'latest', the role fetches the newest release from GitHub
mailpit_version: '1.20.0'  # or 'latest'

# Service user/group
mailpit_service_user: mailpit
mailpit_service_group: mailpit

# Enable/disable service
mailpit_enabled: true
```

### SMTP Configuration

```yaml
# SMTP server bind address (default: localhost only)
mailpit_smtp_bind: 127.0.0.1:1025

# SMTP authentication settings
mailpit_smtp_auth_accept_any: false
mailpit_smtp_auth_allow_insecure: false
```

### Web UI Configuration

```yaml
# Web UI bind address (default: localhost only)
mailpit_ui_bind: 127.0.0.1:8025

# Maximum number of messages to store
mailpit_max_messages: 500

# Use message dates instead of receive time
mailpit_use_message_dates: false
```

### nginx Configuration

```yaml
# Virtual host server name (subdomain recommended)
mailpit_vhost_server: mail.local

# Deployment mode selection
# '/' = Subdomain deployment: creates dedicated vhost via nginx_mono
# '/mail/' = Path-based deployment: creates nginx include file only
# For path-based: user must include in existing vhost via vhost_includes: [mailpit]
mailpit_webroot: '/'

# HTTP basic auth users (optional)
mailpit_vhost_users: []

# SSL/TLS configuration
mailpit_vhost_letsencrypt: false
mailpit_vhost_ssl_cert: ''

# Zabbix monitoring
mailpit_vhost_for_zabbix: false
```

## Dependencies

None (nginx_mono is automatically included for web interface)

## Example Playbook

### Basic Usage

```yaml
- hosts: development
  become: true
  roles:
    - role: alphanodes.setup.mailpit
      vars:
        mailpit_vhost_server: mail.dev.example.com
```

### With HTTP Basic Auth

```yaml
- hosts: development
  become: true
  roles:
    - role: alphanodes.setup.mailpit
      vars:
        mailpit_vhost_server: mail.dev.example.com
        mailpit_vhost_users:
          - user: developer
            password: secret123
```

### With Let's Encrypt SSL

```yaml
- hosts: development
  become: true
  roles:
    - role: alphanodes.setup.mailpit
      vars:
        mailpit_vhost_server: mail.dev.example.com
        mailpit_vhost_letsencrypt: true
```

### Always Use Latest Version

```yaml
- hosts: development
  become: true
  roles:
    - role: alphanodes.setup.mailpit
      vars:
        mailpit_version: latest  # Always install newest release
        mailpit_vhost_server: mail.dev.example.com
```

### Path-Based Deployment (Without Subdomain)

For customers without a dedicated subdomain, mailpit can run under a path using nginx includes.

**Step 1**: Deploy mailpit with path-based configuration:

```yaml
- hosts: production
  become: true
  roles:
    - role: alphanodes.setup.mailpit
      vars:
        mailpit_webroot: '/mail/'  # Creates /etc/nginx/mailpit.conf include file
        mailpit_vhost_users:
          - user: admin
            password: secure123
```

**Step 2**: Include mailpit in your existing service vhost (e.g., Redmine):

```yaml
redmine_instances:
  redmine:
    server_name: example.com
    vhost_includes:
      - mailpit  # Include /etc/nginx/mailpit.conf
    # ... other redmine configuration
```

**Note**: When using path-based deployment:

- mailpit creates ONLY an nginx include file at `/etc/nginx/mailpit.conf`
- NO dedicated vhost is created
- You must include it in an existing vhost via `vhost_includes: [mailpit]`
- Access web UI at: `https://example.com/mail/`
- SMTP remains at: `localhost:1025` (unchanged)
- Useful for migrating from mailcatcher without dedicated subdomain

## Usage with Applications

### Ruby on Rails / Redmine

```yaml
# config/environments/development.rb
config.action_mailer.delivery_method = :smtp
config.action_mailer.smtp_settings = {
  address: 'localhost',
  port: 1025
}
```

### PHP / Drupal

```ini
; php.ini or docker environment
SMTP_HOST=localhost
SMTP_PORT=1025
```

### Node.js / Nodemailer

```javascript
const transport = nodemailer.createTransport({
  host: 'localhost',
  port: 1025,
  secure: false,
  tls: { rejectUnauthorized: false }
});
```

## Accessing Mailpit

After installation:

**Subdomain deployment** (with `mailpit_webroot: '/'`):

- Creates dedicated nginx vhost via nginx_mono
- **Web UI**: `https://mail.dev.example.com` (or your configured vhost)
- **SMTP**: `localhost:1025` (from applications on the same server)
- **API**: `https://mail.dev.example.com/api/v1/` (REST API endpoint)

**Path-based deployment** (with `mailpit_webroot: '/mail/'`):

- Creates nginx include file `/etc/nginx/mailpit.conf` only
- User must include in existing vhost via `vhost_includes: [mailpit]`
- **Web UI**: `https://example.com/mail/` (via existing vhost)
- **SMTP**: `localhost:1025` (unchanged, from applications on the same server)
- **API**: `https://example.com/mail/api/v1/` (REST API endpoint)

## Security Notes

- **SMTP is bound to localhost only by default** - only local applications can send emails
- **Web UI is proxied through nginx** - can be protected with HTTP basic auth
- **Use SSL/TLS in production** - set `mailpit_vhost_letsencrypt: true`
- **Consider using a subdomain** - e.g., `mail.dev.example.com` instead of a path

## Migration from mailcatcher

Mailpit is a modern replacement for mailcatcher with better performance and features:

**mailcatcher (Ruby)**:

```yaml
# Old configuration
smtp_address: localhost
smtp_port: 1025
```

**mailpit (Go)** - same SMTP configuration:

```yaml
# Same SMTP settings work!
smtp_address: localhost
smtp_port: 1025
```

**Advantages over mailcatcher**:

- ✅ Single binary (no Ruby/Gem dependencies)
- ✅ Better performance (Go vs Ruby)
- ✅ Modern web UI with better UX
- ✅ Active development and maintenance
- ✅ Built-in REST API
- ✅ Better search and filtering

## License

MIT

## Author Information

This role was created by [AlphaNodes](https://alphanodes.com/).
