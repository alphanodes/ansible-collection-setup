# Ansible Role: mysql

An Ansible Role that installs Oracle MySQL server from repo.mysql.com on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.mysql
```

## MariaDB Support

Oracle MySQL packages from repo.mysql.com exist for amd64 and i386 only, not for ARM64. For local testing on ARM64 (for example Apple Silicon) or where MariaDB is preferred, set `mysql_backend: mariadb`:

```yaml
    - hosts: all

      vars:
        mysql_backend: mariadb
        mysql_root_password: 'your_root_password'

      roles:
        - alphanodes.setup.mysql
```

This switches packages, configuration paths (`/etc/mysql/mariadb.cnf`), the service name (`mariadb`) and the auth plugin (`mysql_native_password` instead of `caching_sha2_password`), and skips MySQL-only settings like `innodb_redo_log_capacity`.
