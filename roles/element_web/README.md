# Ansible Role: element_web

An Ansible Role that installs the [Element Web](https://github.com/element-hq/element-web) Matrix client on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.element_web
```
