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
