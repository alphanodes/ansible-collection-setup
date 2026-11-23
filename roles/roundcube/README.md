# Ansible Role: roundcube

An Ansible Role that installs [Roundcube](https://roundcube.net/) webmail on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        roundcube_vhost_server: webmail.example.com
        roundcube_vhost_letsencrypt: true

      roles:
        - alphanodes.setup.roundcube
```

## Custom Files

The role picks up optional files from the playbook directory, a file named after the host wins over one named after the first group of the host:

- `files/roundcube/logo/<inventory_hostname or group>.png` for a custom logo
- `files/roundcube/config/<inventory_hostname or group>/config.inc.php` for additional configuration

## Upgrading from 1.6 to 1.7

Roundcube 1.7 only exposes `public_html/` as document root and serves all static files via `static.php`, the role configures nginx accordingly. The custom logo moved from `images/` to `skins/elastic/images/`, the old `images/` directory can be removed after the upgrade. The database schema is updated on the next run, take a database backup before, as there is no way back to 1.6 afterwards.
