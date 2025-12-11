# Certbot Role

Installs and configures Certbot for Let's Encrypt certificate management on Debian/Ubuntu systems.

This role is a drop-in replacement for `geerlingguy.certbot` with simplified configuration
focused on Debian-based systems with systemd.

## Requirements

- Debian 12+ or Ubuntu 24.04+
- For webroot method: A running web server (nginx recommended)

## Role Variables

### Auto-Renewal Configuration

The role uses Debian's built-in `certbot.timer` systemd timer for automatic renewal.
The timer runs twice daily with a random delay up to 12 hours to prevent thundering herd.

```yaml
# Enable automatic certificate renewal via systemd timer
certbot_auto_renew: true

# Remove legacy cron jobs from previous installations
certbot_remove_cron_job: true

# Global deploy hook - runs after successful certificate renewal
# Example: "systemctl reload nginx"
certbot_deploy_hook: ""
```

### Certificate Creation

```yaml
# Use Let's Encrypt staging servers (for testing)
certbot_testmode: false

# Enable HSTS header
certbot_hsts: false

# Create certificates if they don't exist
certbot_create_if_missing: false

# Method: 'standalone' or 'webroot'
certbot_create_method: webroot

# Extra arguments for certbot command
certbot_create_extra_args: ""

# Admin email for Let's Encrypt notifications
certbot_admin_email: email@example.com

# Expand existing certificates with new domains
certbot_expand: false

# Default webroot directory for acme-challenge
certbot_webroot: /var/www/letsencrypt
```

### Certificate Definitions

```yaml
certbot_certs:
  - name: example.com
    email: admin@example.com
    webroot: "/var/www/html/"
    domains:
      - example.com
      - www.example.com
    deploy_hook: "systemctl reload nginx"
  - domains:
      - example2.com
```

### Standalone Mode Configuration

For standalone mode, certbot needs to bind to port 80. These services will be
stopped before and started after certificate creation:

```yaml
certbot_create_standalone_stop_services:
  - nginx
```

### nginx Integration

```yaml
# Create acme-challenge nginx include file
certbot_nginx_integration: true
```

When enabled, creates `/etc/nginx/acme-challenge.conf` that can be included in vhosts:

```nginx
include /etc/nginx/acme-challenge.conf;
```

## Dependencies

- `alphanodes.setup.common`

## Example Playbook

### Basic Installation with Auto-Renewal

```yaml
- hosts: webservers
  roles:
    - role: alphanodes.setup.certbot
```

### Create Certificates with Webroot Method

```yaml
- hosts: webservers
  vars:
    certbot_create_if_missing: true
    certbot_create_method: webroot
    certbot_admin_email: admin@example.com
    certbot_certs:
      - domains:
          - example.com
          - www.example.com
        deploy_hook: "systemctl reload nginx"
  roles:
    - role: alphanodes.setup.certbot
```

### Standalone Mode (Without Web Server)

```yaml
- hosts: mailservers
  vars:
    certbot_create_if_missing: true
    certbot_create_method: standalone
    certbot_admin_email: admin@example.com
    certbot_create_standalone_stop_services: []
    certbot_certs:
      - domains:
          - mail.example.com
  roles:
    - role: alphanodes.setup.certbot
```

### Integration with nginx_mono

```yaml
- hosts: webservers
  vars:
    certbot_create_if_missing: true
    certbot_admin_email: admin@example.com
    certbot_certs:
      - domains:
          - app.example.com

    # nginx_mono vhost configuration
    nginx_mono_service_name: myapp
    nginx_mono_service_config:
      server_name: app.example.com
      letsencrypt: true
      vhost_includes:
        - acme-challenge
  roles:
    - role: alphanodes.setup.certbot
    - role: alphanodes.setup.nginx_mono
```

## Auto-Renewal Details

This role uses Debian's built-in `certbot.timer` systemd timer instead of cron:

- **Schedule**: Runs twice daily (00:00 and 12:00)
- **Random delay**: Up to 12 hours (`RandomizedDelaySec=43200`)
- **Service**: `certbot.service` runs `certbot renew --quiet`

Check timer status:

```bash
systemctl status certbot.timer
systemctl list-timers certbot.timer
```

## Certificate Paths

Certificates are stored in the standard Let's Encrypt locations:

- Certificate: `/etc/letsencrypt/live/<domain>/fullchain.pem`
- Private Key: `/etc/letsencrypt/live/<domain>/privkey.pem`
- Chain: `/etc/letsencrypt/live/<domain>/chain.pem`

## Migration from geerlingguy.certbot

This role is designed as a drop-in replacement for `geerlingguy.certbot` with a focus
on Debian-based systems using systemd.

### Removed Variables

The following variables from `geerlingguy.certbot` are **no longer supported**:

| Removed Variable | Reason |
| ---------------- | ------ |
| `certbot_auto_renew_user` | Systemd timer runs as root |
| `certbot_auto_renew_hour` | Systemd timer uses built-in schedule |
| `certbot_auto_renew_minute` | Systemd timer uses built-in schedule |
| `certbot_auto_renew_options` | Replaced by `certbot_deploy_hook` |
| `certbot_install_method` | Only package installation supported |
| `certbot_repo` | No PPA/snap support |
| `certbot_package` | Always uses `certbot` package |

### New Variables

| New Variable | Description |
| ------------ | ----------- |
| `certbot_deploy_hook` | Global deploy hook command (runs after renewal) |
| `certbot_nginx_integration` | Create nginx acme-challenge config |
| `certbot_remove_cron_job` | Remove legacy cron jobs |

### Migration Steps

1. **Remove obsolete variables** from your inventory:

   ```yaml
   # Remove these:
   # certbot_auto_renew_user: root
   # certbot_auto_renew_hour: 3
   # certbot_auto_renew_minute: 30
   # certbot_auto_renew_options: "--quiet --no-self-upgrade"
   ```

2. **Add deploy hook** if you need to reload services after renewal:

   ```yaml
   # Add this:
   certbot_deploy_hook: "systemctl reload nginx"
   ```

3. **Update role reference** in your playbooks:

   ```yaml
   # Change from:
   - role: geerlingguy.certbot

   # To:
   - role: alphanodes.setup.certbot
   ```

### Key Differences

- **Systemd timer instead of cron**: Uses Debian's built-in `certbot.timer`
- **No snap/source installation**: Only apt package installation
- **Deploy hooks**: Global hook via `certbot_deploy_hook` or per-cert hooks
- **nginx integration**: Optional `acme-challenge.conf` include file

## License

MIT

## Author Information

AlphaNodes - Based on geerlingguy.certbot
