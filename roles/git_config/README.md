# Ansible Role: Git config

Setup git config on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        git_config_settings:
          - name: safe.directory
            value: '*'
            scope: global

      tasks:
        ansible.builtin.include_role:
          name: alphanodes.setup.git_config
```
