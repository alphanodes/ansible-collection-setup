# Ansible Role: nginx_mono

An Ansible Role that sets up [Nginx](https://nginx.org/) vhosts from a single, self-contained template set on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.nginx_mono
```

## Configuration Conventions

Structured directive lists must NOT include a trailing semicolon, the templates append `;` and the role fails fast if an entry ends with one. This applies to `additional_headers`, `fastcgi_params`, `proxy_headers`, `rewrite_lines`, `proxy_redirect`, `locations[].action`, `locations[].actions` and `mappings[].actions`/`mappings[].rewrite_lines`.

Raw includes (for example via `vhost_includes`) and `locations[].raw_actions` are passed through as-is, so they need complete directives including `;`. Use `raw_actions` for brace blocks that must not get a `;` appended:

```yaml
    locations:
      - name: "= /favicon.ico"
        actions:
          - "log_not_found off"
          - "access_log off"
      - name: "= /"
        raw_actions:
          - "if ( $http_user_agent ~ ^DavClnt ) { return 302 /remote.php/webdav/$is_args$args; }"
```

## Debugging Vhost Output

Set `nginx_mono_show_vhost: true` to print the rendered `/etc/nginx/sites-available/<service>.conf` right after rendering, before the vhost gets enabled. Use it in test environments only, the output may contain sensitive paths or values.
