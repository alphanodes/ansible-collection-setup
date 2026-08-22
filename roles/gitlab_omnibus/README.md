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

Notes

- External URL/TLS can be fronted by nginx/nginx_mono if desired.
