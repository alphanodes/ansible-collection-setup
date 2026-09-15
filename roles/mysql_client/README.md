# Ansible Role: mysql_client

An Ansible Role that installs the Oracle MySQL client from repo.mysql.com on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.mysql_client
```

## MariaDB Support

Oracle MySQL packages from repo.mysql.com exist for amd64 and i386 only, not for ARM64. For local testing on ARM64 (for example Apple Silicon) or where MariaDB is preferred, set `mysql_backend: mariadb` to install the MariaDB client packages instead:

```yaml
    - hosts: all

      vars:
        mysql_backend: mariadb

      roles:
        - alphanodes.setup.mysql_client
```
