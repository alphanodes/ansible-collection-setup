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
