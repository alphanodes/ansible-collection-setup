# Ansible Role: Glances

Setup [Glances](https://github.com/nicolargo/glances) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        glances_with_pip: true

      roles:
        - alphanodes.setup.glances
```
