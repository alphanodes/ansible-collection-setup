# Ansible Role: HedgeDoc

Installs [HedgeDoc](https://hedgedoc.org/) on Debian and Ubuntu servers without docker.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        hedgedoc_vhost_server: myvhost.mydomain.com

      roles:
        - alphanodes.setup.hedgedoc
```
