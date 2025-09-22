# Ansible Role: Nginx

Setup [Nginx](https://www.nginx.com/) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.nginx_nono
```
