# Ansible Role: grafana

An Ansible Role that installs [Grafana](https://grafana.com/) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.grafana
```
