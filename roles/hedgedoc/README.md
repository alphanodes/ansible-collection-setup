# Ansible Role: HedgeDoc

Installs [HedgeDoc](https://hedgedoc.org/) on Debian and Ubuntu servers without docker.

## Requirements

HedgeDoc 1.12.0 and later require node 20.17 or later. The role installs node
with the `nodejs` role and fails early if the installed version is too old.

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
