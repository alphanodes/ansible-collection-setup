# Ansible Role: golang

An Ansible Role that installs Go language on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        golang_version: '1.27.4'

      roles:
        - alphanodes.setup.golang
```
