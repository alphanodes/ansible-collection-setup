# Ansible Role: python

An Ansible Role that installs Python with pip and virtualenv on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        python_pip_packages:
          - name: docker
          - name: awscli

      roles:
        - alphanodes.setup.python
```
