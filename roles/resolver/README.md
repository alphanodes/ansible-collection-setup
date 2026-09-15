# Ansible Role: resolver

An Ansible Role that configures DNS resolution via a static `/etc/resolv.conf` or systemd-resolved, optionally with a local unbound cache, on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        resolver_mode: static
        resolver_with_unbound: true
        resolver_nameservers:
          - 1.1.1.1
          - 1.0.0.1

      roles:
        - alphanodes.setup.resolver
```

With `resolver_with_unbound: true` the role includes `alphanodes.setup.unbound` and points the resolver to `127.0.0.1`, with `resolver_nameservers` as fallback.
