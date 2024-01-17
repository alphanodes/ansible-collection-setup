# Ansible Role: rvm

An Ansible Role that installs [rvm](https://rsync.samba.org/) and manage ruby version on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        rvm1_rubies: ['ruby-2.2.5','ruby-2.3.1'],
        rvm1_install_flags: '--auto-dotfiles',     # Remove --user-install from defaults
        rvm1_install_path: /usr/local/rvm,         # Set to system location
        rvm1_user: root

      roles:
        - alphanodes.setup.rvm
```
