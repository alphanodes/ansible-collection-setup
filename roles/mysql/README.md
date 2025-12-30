# Ansible Role: MySQL server

Installs MySQL server on Debian and Ubuntu servers.

## Default Behavior

By default, this role installs **Oracle MySQL** from the official MySQL APT repository
(repo.mysql.com). This is the recommended setup for production environments.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
- hosts: all

  roles:
    - alphanodes.setup.mysql
```

## MariaDB Support (Alternative)

This role also supports **MariaDB** as an alternative to Oracle MySQL. This is particularly
useful for:

- Local development/testing on ARM64 (Apple Silicon) where Oracle MySQL packages are not available
- Environments where MariaDB is preferred

### Important Differences

| Feature | Oracle MySQL | MariaDB |
|---------|--------------|---------|
| Auth Plugin | `caching_sha2_password` | `mysql_native_password` |
| Config File | `/etc/mysql/mysql.cnf` | `/etc/mysql/mariadb.cnf` |
| Service Name | `mysql` | `mariadb` |
| InnoDB Redo Log | `innodb_redo_log_capacity` | Not supported |

### MariaDB Configuration

To use MariaDB instead of Oracle MySQL, set `mysql_backend: mariadb`:

```yaml
- hosts: all
  vars:
    mysql_backend: mariadb
    mysql_root_password: 'your_root_password'

  roles:
    - alphanodes.setup.mysql
```

This automatically configures:

- MariaDB package names (`mariadb-server`, `mariadb-client`)
- MariaDB configuration paths
- MariaDB service name
- `mysql_native_password` authentication plugin
- Disables MySQL 8.0+ specific settings (like `innodb_redo_log_capacity`)

### ARM64 Limitation

Oracle MySQL packages from repo.mysql.com are only available for **amd64** and **i386**
architectures. There are **no ARM64 packages** available. For local testing on Apple Silicon
(M1/M2/M3), use the MariaDB configuration above.
