# Ansible Role: alloy

An Ansible Role that installs [Grafana Alloy](https://grafana.com/docs/alloy/) and ships logs to Loki on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        alloy_loki_url: https://loki.example.com
        alloy_basic_pass: secret

      roles:
        - alphanodes.setup.alloy
```
