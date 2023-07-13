# Ansible Role: Jekyll

Installs [Jekyll](https://jekyllrb.com/) on Debian and Ubuntu servers without docker.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.jekyll
```
