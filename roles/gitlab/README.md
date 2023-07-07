# Ansible Role: gitlab

Setup GitLab source installation (without docker)

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

## Example Playbook

```yaml
    - hosts: yourhost
      vars:
        barman_postgresql_password: yoursecretpassword
      roles:
        - alphanodes.setup.gitlab
```
