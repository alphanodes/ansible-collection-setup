# Ansible Role: sphinx

An Ansible Role that installs [Sphinx](https://www.sphinx-doc.org) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.sphinx
```
