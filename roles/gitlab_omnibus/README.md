# Ansible Role: gitlab_omnibus

An Ansible Role that installs [GitLab](https://about.gitlab.com/) Omnibus on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        gitlab_nginx_blocked_user_agents:
          - GPTBot
          - ClaudeBot

      roles:
        - alphanodes.setup.gitlab_omnibus
```

## GitLab Pages

Sites are served as `<namespace>.<pages domain>`, so TLS needs a wildcard certificate from the `certbot` role with `certbot_create_method: dns`:

```yaml
gitlab_pages_enabled: true
gitlab_pages_domain: pages.example.com
gitlab_pages_nginx_ssl_certificate: /etc/letsencrypt/live/pages.example.com/fullchain.pem
gitlab_pages_nginx_ssl_certificate_key: /etc/letsencrypt/live/pages.example.com/privkey.pem
```

Run the `certbot` role before this one, the bundled nginx does not start without the certificate.

The pages vhost only matches the subdomains, the pages domain itself falls through to the default server with the GitLab certificate. Adding `pages.example.com` to the wildcard certificate alone changes nothing, add it to `gitlab_letsencrypt_alt_names` as well if the name has to present a matching certificate.

With `gitlab_pages_access_control: true` private projects stay private. GitLab registers the OAuth application itself and redirects logins through `projects.<pages domain>`, which the wildcard DNS record and certificate already cover.
