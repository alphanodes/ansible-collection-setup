# Ansible Role: certbot

An Ansible Role that installs Certbot and manages Let's Encrypt certificates on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        certbot_create_if_missing: true
        certbot_admin_email: admin@example.com
        certbot_certs:
          - domains:
              - example.com
              - www.example.com
            deploy_hook: systemctl reload nginx

      roles:
        - alphanodes.setup.certbot
```

## nginx Integration

With `certbot_nginx_integration: true` (default) the role creates `/etc/nginx/acme-challenge.conf`. Include it in a vhost (with nginx_mono via `vhost_includes: [acme-challenge]`) so the webroot method can answer HTTP-01 challenges.

## Auto-Renewal and Certificate Paths

Renewal uses Debian's built-in `certbot.timer` instead of cron (`systemctl list-timers certbot.timer`). Certificates are stored in the standard locations `/etc/letsencrypt/live/<domain>/fullchain.pem` and `privkey.pem`.

## Switching from standalone

Existing certificates keep their authenticator and any `pre_hook`/`post_hook` in `/etc/letsencrypt/renewal/<name>.conf`, the role does not issue them again when `certbot_create_method` changes. certbot runs the stop/start hooks in `/etc/letsencrypt/renewal-hooks/` on every renewal, whatever the authenticator. So the role keeps them as long as any certificate still renews with standalone, and removes them once none does. A host with standalone and webroot certificates gets a warning, because the hooks stop nginx during the webroot validation as well. Issue the standalone certificates again with the new method to finish the switch.

## Migration from geerlingguy.certbot

The role is a drop-in replacement for `geerlingguy.certbot`, reduced to apt packages and systemd. Change the role reference to `alphanodes.setup.certbot` and remove these variables from your inventory, they are no longer supported:

- `certbot_auto_renew_user`, `certbot_auto_renew_hour`, `certbot_auto_renew_minute`: the systemd timer runs as root on its own schedule
- `certbot_auto_renew_options`: use `certbot_deploy_hook` or a per certificate `deploy_hook` instead
- `certbot_install_method`, `certbot_repo`, `certbot_package`: only the apt package is supported
