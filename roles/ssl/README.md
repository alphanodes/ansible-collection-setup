# Ansible Role: ssl

An Ansible Role that installs ssl certificates on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        ssl_certs:
          - name: vhost1
          - name: vhost2

      roles:
        - alphanodes.setup.ssl
```
