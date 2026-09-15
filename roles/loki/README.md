# Ansible Role: loki

An Ansible Role that installs [Grafana Loki](https://grafana.com/oss/loki/) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.loki
```
