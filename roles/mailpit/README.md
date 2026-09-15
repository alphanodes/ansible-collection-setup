# Ansible Role: mailpit

An Ansible Role that installs the email testing tool [Mailpit](https://github.com/axllent/mailpit) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        mailpit_vhost_server: mail.dev.example.com
        mailpit_vhost_users:
          - user: developer
            password: secret

      roles:
        - alphanodes.setup.mailpit
```

Applications on the same server send mail to `localhost:1025`, the web UI (and the REST API below `/api/v1/`) is served through nginx.

## Path-Based Deployment

Without a dedicated subdomain, set `mailpit_webroot: '/mail/'`. The role then creates no vhost, only the include file `/etc/nginx/mailpit.conf`, which has to be added to an existing vhost:

```yaml
    - hosts: all

      vars:
        mailpit_webroot: '/mail/'
        redmine_instances:
          redmine:
            server_name: example.com
            vhost_includes:
              - mailpit

      roles:
        - alphanodes.setup.mailpit
        - alphanodes.setup.redmine
```

The web UI is then available at `https://example.com/mail/`, SMTP stays at `localhost:1025`.
