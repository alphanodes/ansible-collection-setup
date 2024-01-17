# Ansible Role: WordPress

Setup [WordPress](https://wordpress.com) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

    - vars:
      wordpress_instances:
        - name: wordpress
          dir: /srv/wordpress
          server_name: www.mywordpress.com

      roles:
        - alphanodes.setup.wordpress
```
