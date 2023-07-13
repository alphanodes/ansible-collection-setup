# Ansible Role: CIFS mount

Setup CIFS mount on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.cifs_mount
```
