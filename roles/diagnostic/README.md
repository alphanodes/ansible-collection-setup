# Ansible Role: Diagnostic tools

Setup diagnostic tools on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        diagnostic_with_btop: true
        diagnostic_with_glances: true
        diagnostic_with_htop: true

      roles:
        - alphanodes.setup.diagnostic
```
