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

## Adding extra systemd directives

The role hardcodes the most common fields (dependencies, environment,
exec_start, syslog_identifier, ...). Anything else - hardening, resource
limits, custom unit options - goes through `unit_extra` / `service_extra`
as raw systemd syntax:

```yaml
    timers:
      app_cleanup:
        exec_start: /usr/local/bin/cleanup
        on_calendar: '*-*-* 02:00:00'
        unit_extra: |
          Documentation=man:cleanup(1)
        service_extra: |
          User=app
          PrivateTmp=yes
          ProtectSystem=strict
          ReadWritePaths=/var/lib/app
          MemoryMax=512M
```

Use `unit_extra` for `[Unit]` directives and `service_extra` for
`[Service]` directives. systemd accepts both `yes`/`no` and `true`/`false`
for booleans.
