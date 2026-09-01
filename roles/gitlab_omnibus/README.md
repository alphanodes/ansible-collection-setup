# Role: gitlab_omnibus

Summary

- Installs and configures GitLab Omnibus on Debian/Ubuntu.

Supported platforms

- Debian, Ubuntu

Dependencies

- No external dependencies outside this collection.

Variables

- See `defaults/main.yml` and `vars/` for configurable options.

Blocking crawlers

Aggressive AI crawlers request every commit SHA combined with every file. Those
URLs are unique and therefore uncacheable, and each one renders a full Rails
view, so a single crawler can occupy most of the available Puma slots on a
public instance. GitLab's unauthenticated rate limit does not stop them,
because it counts per single IP while these crawlers spread their requests
across whole IPv6 prefixes.

Set `gitlab_nginx_blocked_user_agents` to reject them in nginx with HTTP 403,
before the request ever reaches Puma:

```yaml
gitlab_nginx_blocked_user_agents:
  - meta-externalagent
  - GPTBot
  - ClaudeBot
  - Bytespider
  - Amazonbot
  - PerplexityBot
  - CCBot
```

Entries are case-insensitive regex fragments matched against the full
`User-Agent` header, so a plain substring is enough. This also catches crawlers
that disguise themselves inside a browser-like User-Agent. The list is empty by
default, so nothing is blocked unless configured.

Note that `robots.txt` is not an alternative here: GitLab does not disallow
`/blob/`, `/commits/` or `/tree/` there, and honouring it is voluntary anyway.

GitLab Pages

Pages runs behind the bundled nginx by default (`gitlab_pages_behind_nginx`),
which proxies to the pages daemon. It therefore shares the IP address of the
GitLab instance and needs no address of its own. The alternative - the daemon
binding `gitlab_pages_external_http` and `gitlab_pages_external_https` itself -
is only required for user-supplied custom domains, and it needs a secondary IP
because the bundled nginx already holds port 80 and 443.

Sites are served as `<namespace>.<pages domain>`, so TLS needs a wildcard
certificate. GitLab's built-in Let's Encrypt integration cannot supply it: it
only performs the HTTP-01 challenge, which Let's Encrypt does not accept for
wildcards. Use the `certbot` role with `certbot_create_method: dns` for the
certificate and point the role at it:

```yaml
gitlab_pages_enabled: true
gitlab_pages_domain: pages.example.com
gitlab_pages_nginx_ssl_certificate: /etc/letsencrypt/live/pages.example.com/fullchain.pem
gitlab_pages_nginx_ssl_certificate_key: /etc/letsencrypt/live/pages.example.com/privkey.pem
```

GitLab builds the pages vhost with `server_name ~^(?<group>.*)\.pages\.example\.com$`,
so it answers for the subdomains only. The pages domain itself is not matched
by that regex and falls through to the default server, which answers with the
GitLab instance's own certificate. Putting `pages.example.com` into the
certificate next to the wildcard therefore changes nothing on its own - it is
only worth doing as groundwork for `namespace_in_path`, or alongside adding the
name to `gitlab_letsencrypt_alt_names` so the default server presents a
certificate that matches it.

Run the `certbot` role before this one: without the certificate the bundled
nginx does not start. The two certificate paths do not collide, because GitLab
only adds the pages domain to its own Let's Encrypt certificate in
`namespace_in_path` mode, which the wildcard layout does not use.

With `gitlab_pages_access_control: true` private projects stay private, which
matters as soon as `gitlab_pages_artifacts_server` exposes job artifacts.
GitLab registers the OAuth application itself and generates the credentials, so
none have to be configured here. Logins are redirected through
`projects.<pages domain>`, which the wildcard DNS record and certificate
already cover.

Notes

- External URL/TLS can be fronted by nginx/nginx_mono if desired.
