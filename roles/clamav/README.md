# Ansible Role: clamav

An Ansible Role that installs and configures [ClamAV](https://www.clamav.net/) antivirus scanner on Debian and Ubuntu.

## Features

- Installs ClamAV daemon (clamd) and freshclam virus database updater
- Configures Unix socket for efficient communication
- Sets up systemd timer for automated virus database updates
- Configurable resource limits to prevent excessive memory usage
- Logging to systemd journal by default
- EICAR test virus detection verification in Molecule tests

## Requirements

- Debian 12 (Bookworm) or Debian 13 (Trixie)
- Ubuntu 24.04 (Noble)
- Minimum 512MB RAM (recommended: 1GB+ for production)

## Role Variables

### ClamAV Daemon Configuration

Available variables can be found in [defaults/main.yml](defaults/main.yml)

Key variables:

```yaml
# Socket configuration
clamav_socket_path: /var/run/clamav/clamd.ctl
clamav_socket_group: clamav
clamav_socket_mode: '0660'

# Resource limits (prevents excessive memory usage)
clamav_max_threads: 12
clamav_max_file_size: 100M
clamav_max_scan_size: 400M
clamav_stream_max_length: 100M

# Logging
clamav_log_syslog: true
clamav_log_facility: LOG_LOCAL6

# Service configuration
clamav_service_enabled: true
clamav_service_state: started
```

### Freshclam Configuration

```yaml
# Update frequency
clamav_freshclam_on_calendar: hourly
clamav_freshclam_randomized_delay_sec: 900
clamav_freshclam_checks_per_day: 24

# Database mirrors
clamav_freshclam_database_mirror:
  - database.clamav.net
```

## Integration with Redmine Plugin

This role is designed to work with the `redmine_clamav` plugin, which communicates directly with clamd via Unix socket using the INSTREAM protocol.

### Setup Steps

1. Deploy this role to install and configure ClamAV
1. Add the Redmine puma user to the `clamav` group in your Redmine role:

   ```yaml
   - name: Add Redmine puma user to clamav group
     ansible.builtin.user:
       name: "{{ redmine_puma_user }}"
       groups: clamav
       append: true
   ```

1. Configure the Redmine plugin to use the Unix socket (default: `/var/run/clamav/clamd.ctl`)

The plugin will automatically detect and use the socket for virus scanning of uploaded attachments.

## Removing ClamAV

To completely remove ClamAV from a system:

```yaml
- hosts: all
  roles:
    - role: alphanodes.setup.clamav
      vars:
        clamav_remove: true
        clamav_remove_database: true  # Also remove virus database (default: true)
```

This will:

- Stop and disable all ClamAV services
- Remove systemd service and timer files
- Remove configuration files
- Uninstall ClamAV packages
- Remove virus database directory (if `clamav_remove_database: true`)

## Example Playbook

Basic usage:

```yaml
- hosts: all
  roles:
    - alphanodes.setup.clamav
```

With custom configuration:

```yaml
- hosts: all
  roles:
    - role: alphanodes.setup.clamav
      vars:
        clamav_max_file_size: 200M
        clamav_max_scan_size: 800M
        clamav_freshclam_on_calendar: "*/2h"  # Update every 2 hours
```

## Testing

The role includes comprehensive Molecule tests that verify:

- ClamAV daemon installation and startup
- Unix socket creation and permissions
- Virus database updates via freshclam
- EICAR test virus detection (standard antivirus test file)
- Service health checks

Run tests with:

```bash
MOLECULE_DISTRO=debian12 molecule test -s clamav
MOLECULE_DISTRO=ubuntu2404 molecule test -s clamav
```

## Security Considerations

- ClamAV daemon runs as user `clamav` with restricted permissions
- Unix socket is readable/writable only by `clamav` group members
- Systemd hardening options applied (PrivateTmp, ProtectHome, etc.)
- Resource limits configured to prevent DoS via memory exhaustion
- Regular automatic virus database updates via systemd timer

## Performance Notes

- ClamAV typically uses 200MB-1GB RAM depending on loaded signatures
- Socket-based communication (INSTREAM) is more efficient than binary calls
- Virus database updates (freshclam) run hourly with randomized delay to reduce mirror load
- Initial database download may take several minutes on first run

## License

Apache License 2.0

## Author Information

This role was created by [AlphaNodes](https://alphanodes.com/).
