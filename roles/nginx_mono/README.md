# Ansible Role: nginx_mono

Setup [Nginx](https://www.nginx.com/) vhosts from a single, self‑contained template set.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Configuration Conventions

- Structured directive lists must NOT include trailing semicolons — the templates append `;` for you. This applies to:
  - `additional_headers`: list of `Name Value` → renders as `add_header ...;`
  - `fastcgi_params`: list of `Name Value` → renders as `fastcgi_param ...;`
  - `proxy_headers`: list of `Name Value` → renders as `proxy_set_header ...;`
  - `rewrite_lines`: list of rewrite arguments → renders as `rewrite ...;`
  - `proxy_redirect`: single value (no `;`) → renders as `proxy_redirect ...;`
  - `locations[].action` and `locations[].actions`: entries without `;`
  - `mappings[].actions` and `mappings[].rewrite_lines`: entries without `;`

- Raw includes (for example via `vhost_includes`) are passed through as-is: provide complete Nginx directives including the trailing `;` — raw is raw.

The role validates structured fields and fails fast if any entry ends with `;` (clear error messages). Further variable details are commented directly in `defaults/main.yml`.

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.nginx_mono
```
