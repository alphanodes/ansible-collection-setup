# Ansible Role: systemd_timer

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook for add timer

```yaml
    - hosts: all

      vars:
        timers:
          microcache_directory:
            exec_start: /usr/bin/install -g www-data -o www-data -d /run/my_cachezone
            on_boot_sec: 5s
            before_service: nginx.service
            env:
              RAILS_ENV: production
              YOUR_VAR: 1

      roles:
        - alphanodes.setup.systemd_timer
```

## Example Playbook for remove timer

```yaml
    - hosts: all

      vars:
        timers:
          microcache_directory:
            state: absent
      roles:
        - alphanodes.setup.systemd_timer
```
