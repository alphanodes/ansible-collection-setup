# Ansible Role: Rspamd

[![alphanodes.setup.rspamd](https://github.com/alphanodes/ansible.setup/actions/workflows/rspamd.yml/badge.svg)](https://github.com/alphanodes/ansible.setup/actions/workflows/rspamd.yml)

Install and configure Rspamd spam filtering system with DKIM signing support.

## Description

This role installs and configures Rspamd, a modern spam filtering system with built-in DKIM signing, ARC support, and Redis integration for learning and statistics.

**Key Features:**

- Rspamd installation from official repositories
- Automatic DKIM key generation and configuration
- Redis integration for statistics and learning
- Web UI with password protection
- Nginx vhost support (optional)
- Whitelist/blacklist management
- Milter protocol support for Postfix integration

## Requirements

- Ansible 2.18+
- Debian 11+ or Ubuntu 22.04+
- Redis server (automatically installed as dependency)

## Role Variables

### Required Variables

```yaml
# Controller password (generate with: rspamadm pw)
rspamd_worker_controller_password: '$2$...'
```

### DKIM Configuration

DKIM configuration uses the centralized `dkim_domains` dictionary in host_vars.
The dkim role (automatic dependency) generates keys for all domains.

```yaml
# Define in host_vars (e.g., host_vars/mailserver.yml)
dkim_domains:
  example.com:
    selector: mail
    key_size: 2048
  example.org:
    selector: default
    key_size: 2048
```

Rspamd uses the `$domain` variable at runtime for automatic multi-domain DKIM signing.
Keys are generated at `/var/lib/dkim/$domain/{{ selector }}.key`.

### Optional Variables

```yaml
# Enable rspamd service
rspamd_enable_service: true

# Log level (error, warning, notice, info, debug)
rspamd_log_level: warning

# Redis configuration
rspamd_redis_servers: "127.0.0.1"
rspamd_redis_db: 1

# Web UI configuration
rspamd_vhost_server: rspamd.local
rspamd_web_user: rspamd
rspamd_web_password: ''  # Empty = no basic auth

# Whitelist/Blacklist
rspamd_whitelist_ip: []
rspamd_whitelist_from: []
rspamd_blacklist_ip: []
rspamd_blacklist_from: []

# Timeouts of network-bound checks. A scan is capped by task_timeout (8s by
# default), so no single check may be allowed to stall anywhere near that
# long - otherwise one unreachable service delays every message.
rspamd_dns_timeout: 2s
rspamd_dns_retransmits: 2
rspamd_fuzzy_timeout: 2s
rspamd_fuzzy_retransmits: 1
rspamd_fuzzy_servers: ''  # Empty = upstream default server list

# Proxy worker (milter endpoint)
rspamd_proxy_timeout: 120s
rspamd_proxy_max_retries: 5

# Checks skipped for authenticated senders. These rate the sender, which is
# pointless once it has authenticated, and their lookups are the main source
# of stalled outgoing scans. URL blacklists are not part of this and keep
# running in both directions. Empty list = scan authenticated senders fully.
rspamd_authenticated_symbols_disabled:
  - ASN_CHECK
  - RSPAMD_URIBL
  - RSPAMD_EMAILBL

# Neural network module. Off by default: its ANN profile is keyed by the set
# of active symbols, so every configuration change invalidates it and sample
# collection restarts. A config-managed host never reaches a trained model.
rspamd_neural_enabled: false
```

### Bayes classifier

Rspamd ships the bayes classifier enabled but never trains it. Without training
the statfiles stay empty, `BAYES_HAM` and `BAYES_SPAM` never reach `min_learns`
(200 per class), and the classifier contributes nothing to any verdict while
still being queried for every message. Check with `rspamc stat`:

```text
Statfile: BAYES_SPAM ... learned: 0
Statfile: BAYES_HAM  ... learned: 0
```

Autolearn trains the classifier from rspamd's own verdict, so it needs no user
interaction and no IMAP side setup. The trade-off is that it confirms what the
other rules already decided rather than adding an independent signal.

```yaml
# Off by default. Turning it on changes no delivery behaviour, it only starts
# filling the statfiles.
rspamd_bayes_autolearn: true

# Learn as spam from this score upwards
rspamd_bayes_autolearn_spam_threshold: 6.0
# Learn as spam when the message was filed as junk from this score upwards
rspamd_bayes_autolearn_junk_threshold: 4.0
# Learn as ham from this score downwards
rspamd_bayes_autolearn_ham_threshold: -0.5
# Ham vastly outnumbers spam on a normal mail flow. Without a balance guard the
# ham statfile outgrows the spam one and biases every verdict.
rspamd_bayes_autolearn_check_balance: true
rspamd_bayes_autolearn_min_balance: 0.9
```

Verify after a few days that both statfiles are growing:

```bash
rspamc stat | grep -E "Statfile|Messages learned"
```

### Spam header for filtering on the MDA side

Rspamd emits no `X-Spam-Flag`. Its default headers are `X-Spamd-Bar`,
`X-Spam-Level`, `X-Spam-Status` and `Authentication-Results` - and
`X-Spam-Status` is present on every message, spam or not:

```text
X-Spamd-Bar: -----
X-Spam-Status: No, score=-5.65
```

A Sieve rule matching `X-Spam-Flag` therefore never fires and nothing is filed
away. Enable the `spam-header` routine to get an unambiguous marker on every
message that reached the `add_header` action or a stricter one. Rspamd names
this header `Deliver-To: Junk` by default, which most MDAs ignore, so name and
value are set explicitly:

```yaml
rspamd_with_spam_header: true
rspamd_spam_header_name: X-Spam
rspamd_spam_header_value: 'Yes'
```

Authenticated and local senders are skipped by the module itself, so outgoing
mail is never marked.

The dovecot role has to match this exactly, otherwise the header is written but
nothing acts on it:

```yaml
dovecot_spam_header_name: X-Spam
dovecot_spam_header_value: 'Yes'
```

Note that this changes what users see: mail scoring at or above
`rspamd_action_add_header` moves out of the inbox into the Junk folder. Check
`rspamc stat` for the share of messages this affects before enabling it.

### Diagnosing slow scans

Set `rspamd_log_level: info` temporarily. rspamd then writes one
`rspamd_task_write_log` line per message with the total scan time, the DNS
request count and the symbols that fired:

```bash
journalctl -u rspamd --since "-24 hours" -o cat \
  | grep -oE "time: [0-9.]+ms, dns req: [0-9]+"
```

Outgoing mail carries the `LOCAL_OUTBOUND` symbol and can be filtered out
separately. Scan times clustering on an exact value (4000 ms, 8000 ms) point
at a timeout rather than at slow processing: a check whose lookup never gets
answered burns its full timeout budget on every message. A `*_FAIL` symbol
such as `RSPAMD_URIBL_FAIL` names the check that gave up.

Set the level back to `warning` afterwards - `info` logs every single message.

## Dependencies

This role automatically includes:

- `alphanodes.setup.common` - Common setup tasks
- `alphanodes.setup.redis_server` - Redis server for statistics
- `alphanodes.setup.dkim` - DKIM key management (when `dkim_domains` is defined in host_vars)

## Example Playbook

### Basic Setup with DKIM

```yaml
# host_vars/mailserver.yml
dkim_domains:
  example.com:
    selector: mail
    key_size: 2048

# playbook.yml
- hosts: mail_servers
  roles:
    - role: alphanodes.setup.rspamd
      vars:
        rspamd_worker_controller_password: '$2$...'
```

### Advanced Setup

```yaml
# host_vars/mailserver.yml
dkim_domains:
  example.com:
    selector: mail
    key_size: 2048

# playbook.yml
- hosts: mail_servers
  roles:
    - role: alphanodes.setup.rspamd
      vars:
        rspamd_worker_controller_password: '$2$...'
        rspamd_log_level: info
        rspamd_whitelist_ip:
          - 192.168.1.0/24
          - 10.0.0.0/8
        rspamd_vhost_server: spam.example.com
        rspamd_web_user: admin
        rspamd_web_password: 'secure_password_hash'
```

## Postfix Integration

Add to Postfix `/etc/postfix/main.cf`:

```text
# Rspamd milter
smtpd_milters = inet:localhost:11332
non_smtpd_milters = inet:localhost:11332
milter_protocol = 6
milter_mail_macros = i {mail_addr} {client_addr} {client_name} {auth_authen}
milter_default_action = accept
```

## Web UI Access

Access the Rspamd web UI at:

- Without vhost: `http://yourserver:11333`
- With vhost: `https://rspamd.yourdomain.com/` (requires nginx setup)

Login with the password you generated with `rspamadm pw`.

## Generate Controller Password

```bash
# On the target server
rspamadm pw
# Enter your password when prompted
# Copy the hash to rspamd_worker_controller_password
```

## DNS Configuration

After installation with DKIM enabled, add the DNS TXT records:

```bash
# View DKIM public key
cat /var/lib/dkim/example.com/mail.txt

# Verify DNS propagation
dig +short TXT mail._domainkey.example.com
```

## Testing

Run Molecule tests:

```bash
MOLECULE_DISTRO=debian12 molecule test -s rspamd
```

## Service Ports

- **11332**: Milter protocol (Postfix integration)
- **11333**: Web UI and HTTP API
- **11334**: Normal worker (scanning)

## Troubleshooting

### Check Rspamd status

```bash
systemctl status rspamd
rspamc stat
```

### Test DKIM signing

```bash
# Check DKIM configuration
rspamadm dkim_keygen -s mail -d example.com

# Test with email
rspamc --ip 192.168.1.1 < test_email.eml
```

### View logs

```bash
journalctl -u rspamd -f
```

## License

Apache License 2.0

## Author

AlphaNodes
