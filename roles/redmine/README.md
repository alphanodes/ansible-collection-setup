# Ansible Role: redmine

An Ansible Role that installs [Redmine](https://www.redmine.org/) on Debian and Ubuntu servers without Docker.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        redmine_instances:
          redmine1:
            server_name: my_vhost.mydomain.com
            adapter: postgresql
          another_redmine:
            server_name: another-redmine.mydomain.com
            adapter: mysql2

      roles:
        - alphanodes.setup.redmine
```

## Shared Redis

For a shared Redis service, configure `alphanodes.setup.redis_server` once in the playbook and set `redmine_manage_redis: false`. Keep `redmine_with_redis: true` so Redmine continues using Redis. Only the central role should set `redis_server_*` daemon settings; `redmine_redis_url` and per-instance namespaces configure the application connection. `redmine_redis_maxmemory` and `redmine_redis_maxmemory_policy` apply only when this role manages Redis itself.
