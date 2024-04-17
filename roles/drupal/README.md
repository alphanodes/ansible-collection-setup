# Ansible Role: Drupal

Setup [Drupal](https://www.drupal.org/) on Debian and Ubuntu servers without Docker.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

    - vars:
      drupal_instances:
        - name: drupal8
          dir: /srv/drupal8
          server_name: www.mydrupal8.com

      roles:
        - alphanodes.setup.drupal
```
