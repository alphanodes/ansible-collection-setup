# Ansible Role: Nextcloud

Setup [Nextcloud](https://nextcloud.com/) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        nextcloud_vhost_server: myvhost.mydomain.com

      roles:
        - alphanodes.setup.nextcloud
```
