# Ansible Role: Drupal

Setup [Drupal](https://www.drupal.org/) on Debian and Ubuntu servers without Docker.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.drupal
```
