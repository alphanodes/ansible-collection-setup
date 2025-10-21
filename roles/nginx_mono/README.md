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

### Locations: `actions` vs `raw_actions`

When defining custom directives inside a `location` block you have two options:

- `actions` (preferred for simple directives):
  - Provide plain directive fragments without a trailing `;`.
  - The template appends `;` for each entry.
  - Example:

    ```yaml
    locations:
      - name: "= /favicon.ico"
        actions:
          - "log_not_found off"
          - "access_log off"
    ```

- `raw_actions` (use for complex or block directives):
  - Entries are rendered verbatim, without any automatic `;` suffix.
  - Use this when you need multi‑statement lines or brace blocks that must not be followed by `;` by the template.
  - Typical example: conditional redirect for specific user agents (e.g. DavClnt) at `/`:

    ```yaml
    locations:
      - name: "= /"
        raw_actions:
          - "if ( $http_user_agent ~ ^DavClnt ) { return 302 /remote.php/webdav/$is_args$args; }"
    ```

Notes

- Do not mix `actions` and `raw_actions` for the same statement. Choose one depending on whether a trailing `;` must be auto‑appended (`actions`) or must be avoided (`raw_actions`).
- Validation rules that check for trailing semicolons apply to `actions`, not to `raw_actions`, which are passed through as‑is.

## Debugging Vhost Output

- Purpose: Print the fully rendered vhost for troubleshooting.
- Variable: `nginx_mono_show_vhost` (default: `false`, see `defaults/main.yml`).
- Behavior: When set to `true`, the role slurps `/etc/nginx/sites-available/<service>.conf` and outputs its content via a debug task right after rendering, before enabling the symlink.

Example usage (manual include):

```yaml
- name: Setup nginx_mono and show rendered vhost
  ansible.builtin.include_role:
    name: alphanodes.setup.nginx_mono
  vars:
    nginx_mono_show_vhost: true
    nginx_mono_service_name: myservice
    nginx_mono_service_enabled: true
    nginx_mono_service_config:
      server_name: example.test
      root: /var/www/example
```

Notes

- Use only in test environments; the rendered config may include sensitive paths/values.
- Disable again (`false`) once debugging is complete to keep logs concise.

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.nginx_mono
```
