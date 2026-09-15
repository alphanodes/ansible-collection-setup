# Ansible Role: mail_autoconfig

An Ansible Role that serves the Mozilla Autoconfig file for automatic mail client configuration (Thunderbird and compatible clients) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        mail_autoconfig_domain: example.com
        mail_autoconfig_vhost_letsencrypt: true

      roles:
        - alphanodes.setup.mail_autoconfig
```

## DNS Configuration

Mail clients look up `https://autoconfig.<maildomain>/mail/config-v1.1.xml`, so every mail domain needs an A/AAAA record for `autoconfig.<maildomain>` pointing to the server. Verify the result with:

```bash
curl https://autoconfig.example.com/mail/config-v1.1.xml
```

## References

- [Mozilla Autoconfig Specification](https://wiki.mozilla.org/Thunderbird:Autoconfiguration:ConfigFileFormat)
