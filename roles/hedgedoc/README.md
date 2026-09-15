# Ansible Role: hedgedoc

An Ansible Role that installs [HedgeDoc](https://hedgedoc.org/) on Debian and Ubuntu servers without Docker.

## Requirements

HedgeDoc 1.12.0 and later require Node.js 20.17 or later. The role installs Node.js with the `nodejs` role and fails early if the installed version is too old.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        hedgedoc_vhost_server: hedgedoc.example.com

      roles:
        - alphanodes.setup.hedgedoc
```
