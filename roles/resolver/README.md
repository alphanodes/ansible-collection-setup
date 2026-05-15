# alphanodes.setup.resolver

DNS resolver configuration for hosts in this collection. Provides two modes:

- **`static`** (default): Ansible-managed `/etc/resolv.conf`. No daemon. Lowest overhead.
- **`systemd_resolved`**: managed via `systemd-resolved` with override snippets in `/etc/systemd/resolved.conf.d/`.

Both modes can optionally include a local `unbound` DNS cache on `127.0.0.1`
by setting `resolver_with_unbound: true`. When enabled, this role automatically
includes the `alphanodes.setup.unbound` role and configures the chosen backend
to use `127.0.0.1` with `resolver_nameservers` as fallback.

## Variables

| Variable | Default | Description |
|---|---|---|
| `resolver_mode` | `static` | `static` or `systemd_resolved` |
| `resolver_nameservers` | `[]` | Upstream DNS servers (used directly or as fallback when unbound is active) |
| `resolver_with_unbound` | `false` | Install + use local unbound DNS cache on 127.0.0.1 |
| `resolver_systemd_resolved_filename` | `ansible.conf` | Filename of the resolved.conf.d snippet |
| `resolver_search_domains` | `[]` | Search domains |

## Example

Static mode with local unbound cache and public DNS as fallback:

```yaml
resolver_mode: static
resolver_with_unbound: true
resolver_nameservers:
  - 1.1.1.1
  - 1.0.0.1
```

systemd-resolved with internal DNS and search domains:

```yaml
resolver_mode: systemd_resolved
resolver_systemd_resolved_filename: corp.conf
resolver_nameservers:
  - 10.0.0.1
resolver_search_domains:
  - example.internal
```
