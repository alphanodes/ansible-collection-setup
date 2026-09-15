# Ansible Role: rvm

An Ansible Role that installs [rvm](https://rvm.io/) and manages Ruby versions on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        rvm1_rubies:
          - ruby-3.3.6
        rvm1_install_flags: '--auto-dotfiles'
        rvm1_install_path: /usr/local/rvm
        rvm1_user: root

      roles:
        - alphanodes.setup.rvm
```
