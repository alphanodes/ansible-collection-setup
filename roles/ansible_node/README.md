# Ansible Role: Ansible node

Setup Ansible on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        ansible_node_ansible_version: 11.5

      roles:
        - alphanodes.setup.ansible_node
```
