# Ansible Role: zammad

Install one [Zammad](https://zammad.org/) helpdesk per host on Debian 13 or Ubuntu 26.04 using the official stable DEB packages.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml).

## Example Playbook

```yaml
- hosts: helpdesk
  vars:
    zammad_vhost_server: support.example.com
    zammad_db_password: '{{ vault_zammad_db_password }}'
    zammad_vhost_letsencrypt: true
  roles:
    - alphanodes.setup.zammad
```

## Integration and upgrades

The role configures PostgreSQL, Redis and a local Elasticsearch through the collection roles. Set the corresponding `zammad_manage_*` flags to false to use separately managed services. PostgreSQL database provisioning still runs as the local `postgres` account; a remote database must be provisioned separately (not currently supported). Set `postgresql_version` to the desired supported major version (default 18). The matching `postgresql` metapackage must be available in the configured APT repositories.

Provide a TLS certificate through `ssl_certs` or an existing Let's Encrypt certificate. nginx_mono serves static assets and proxies HTTP, `/ws` and `/cable`. The vhost is prepared before package installation so the package cannot activate its plain HTTP example. Upstream package scripts can restart nginx during installation and upgrades.

Set `zammad_with_elasticsearch: false` to disable search indexing. With `zammad_manage_elasticsearch: true`, the Elasticsearch DEB dependency stays installed but its service is stopped, disabled and masked. Set the usage flag back to true to start it and build a missing index. Set `zammad_vhost_users` to protect the entire vhost with HTTP Basic Auth, including WebSocket paths. Gateway Basic Auth credentials are removed from proxied requests; browser sessions authenticate inside Zammad.

The package is held against general APT upgrades. Set `zammad_version` to an exact package version to request a controlled upgrade. Back up through the central backup workflow before upgrades; major versions must not be skipped. Package scripts run migrations. A downgrade is not supported.

Backups are managed separately through the central `alphanodes.tasks.backup` workflow. Include the Zammad PostgreSQL database, `/opt/zammad/config`, `/opt/zammad/storage` and `/etc/zammad`. This role does not create backups or schedule backup jobs. Disabling `zammad_enabled` stops the application and removes its active vhost; data and shared services remain.

Official DEB packages require amd64. The Molecule scenario uses an amd64 Docker platform; native amd64 is recommended because systemd services may fail under ARM host emulation. Budget at least 10 GB RAM for the application, PostgreSQL and local Elasticsearch together.
