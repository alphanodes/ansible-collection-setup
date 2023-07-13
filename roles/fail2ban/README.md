# Ansible Role: Fail2ban

Setup [Fail2ban](https://www.fail2ban.org/) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.fail2ban
```
