# Ansible Role: clamav

An Ansible Role that installs and configures [ClamAV](https://www.clamav.net/) antivirus scanner on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        clamav_socket_users:
          - redmine

      roles:
        - alphanodes.setup.clamav
```

## Integration with Redmine

The `redmine_clamav` plugin talks to clamd directly via the Unix socket (`clamav_socket_path`) using the INSTREAM protocol. Add the user running Redmine to `clamav_socket_users`, so it gets access to the socket, and configure the plugin with the same socket path.

## Removing ClamAV

Set `clamav_remove: true` to stop the services and remove packages, unit files and configuration. The virus database is removed as well unless `clamav_remove_database` is set to `false`.
