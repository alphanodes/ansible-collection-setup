# Ansible Role: go

An Ansible Role that installs Go language on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        golang_version: '1.20.10'
        golang_sha256_checksum: d355c5ae3a8f7763c9ec9dc25153aae373958cbcb60dd09e91a8b56c7621b2fc

      roles:
        - alphanodes.setup.go
```
