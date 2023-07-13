# Ansible Role: unbound

An Ansible Role that installs [unbound](https://github.com/NLnetLabs/unbound) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.unbound
```
