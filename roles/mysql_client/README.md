# Ansible Role: MySQL-Client

Installs MySQL client on Debian and Ubuntu servers.

## Default Behavior

By default, this role installs the **Oracle MySQL client** from the official MySQL APT
repository (repo.mysql.com). This is the recommended setup for production environments.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
- hosts: all

  roles:
    - alphanodes.setup.mysql_client
```

## MariaDB Support (Alternative)

This role also supports **MariaDB client** as an alternative to Oracle MySQL client. This is
particularly useful for:

- Local development/testing on ARM64 (Apple Silicon) where Oracle MySQL packages are not available
- Environments where MariaDB is preferred

### MariaDB Configuration

To use MariaDB client instead of Oracle MySQL client, set `mysql_backend: mariadb`:

```yaml
- hosts: all
  vars:
    mysql_backend: mariadb

  roles:
    - alphanodes.setup.mysql_client
```

This automatically configures MariaDB client package names (`mariadb-client`, `python3-pymysql`).

### ARM64 Limitation

Oracle MySQL packages from repo.mysql.com are only available for **amd64** and **i386**
architectures. There are **no ARM64 packages** available. For local testing on Apple Silicon
(M1/M2/M3), use the MariaDB configuration above.
