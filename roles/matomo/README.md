# Ansible Role: Matomo

Installs [Matomo](https://matomo.org/) on Debian and Ubuntu servers without docker.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        matomo_vhost_server: myvhost.mydomain.com

      roles:
        - alphanodes.setup.matomo
```
