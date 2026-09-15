# Ansible Role: docker

An Ansible Role that installs Docker CE from the official Docker repository on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        docker_with_compose: true

      roles:
        - alphanodes.setup.docker
```
