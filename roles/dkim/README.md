# Ansible Role: dkim

An Ansible Role that generates and manages DKIM keys for one or more mail domains on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        dkim_domains:
          example.com:
            selector: mail
            key_size: 2048

      roles:
        - alphanodes.setup.dkim
```

## DNS Configuration

Keys are stored as `<dkim_base_dir>/<domain>/<selector>.key`, the matching DNS record lands next to it as `<selector>.txt`. Publish that record as TXT entry and verify it:

```bash
cat /var/lib/dkim/example.com/mail.txt
dig +short TXT mail._domainkey.example.com
```

## Key Rotation

1. Set `dkim_force_regenerate: true` and run the playbook
2. Publish the new TXT record
3. Set `dkim_force_regenerate: false` again

Signatures made with the old key fail validation once the record is replaced, so rotate during a quiet period and keep the DNS TTL in mind.
