# Ansible Role: rocketchat

An Ansible Role that installs [rocket.chat](https://www.rocket.chat/) on Debian and Ubuntu servers without Docker.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        rocketchat_vhost_server: my_vhost.mydomain.com

      roles:
        - alphanodes.setup.rocketchat
```
