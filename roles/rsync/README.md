# Ansible Role: rsync

An Ansible Role that installs [rsync](https://rsync.samba.org/) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.rsync
```
