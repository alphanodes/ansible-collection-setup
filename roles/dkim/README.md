# Ansible Role: DKIM

[![alphanodes.setup.dkim](https://github.com/alphanodes/ansible.setup/actions/workflows/dkim.yml/badge.svg)](https://github.com/alphanodes/ansible.setup/actions/workflows/dkim.yml)

Generate and manage DKIM (DomainKeys Identified Mail) keys for email authentication.

## Description

This role generates RSA key pairs for DKIM signing and provides the public keys in DNS-ready format. It supports multiple domains and selectors, making it easy to manage DKIM for complex mail setups.

**Key Features:**

- Generate DKIM RSA key pairs (2048 or 4096 bit)
- Support for multiple domains and selectors
- Automatic DNS TXT record generation
- Secure key storage with proper permissions
- Key rotation support
- Mail-system agnostic (works with Rspamd, OpenDKIM, Postfix, etc.)

## Requirements

- Ansible 2.18+
- Debian 12+ or Ubuntu 24.04+
- `community.crypto` collection (for `openssl_privatekey` module)

## Role Variables

### Required Variables

```yaml
dkim_domains:
  - domain: example.com
    selector: mail
    key_size: 2048
```

### Optional Variables

```yaml
# Base directory for DKIM keys
dkim_base_dir: /var/lib/dkim

# User/Group for key files (override based on your mail system)
dkim_user: root
dkim_group: root

# Default selector if not specified per domain
dkim_default_selector: mail

# Default key size in bits
dkim_default_key_size: 2048

# Force key regeneration (for rotation)
dkim_force_regenerate: false

# Display public keys during playbook run
dkim_show_public_keys: true
```

## Dependencies

None. This role is standalone and can be used with any mail system.

## Example Playbook

### Basic Usage

```yaml
- hosts: mail_servers
  roles:
    - role: alphanodes.setup.dkim
      vars:
        dkim_domains:
          - domain: example.com
            selector: mail
```

### Multiple Domains

```yaml
- hosts: mail_servers
  roles:
    - role: alphanodes.setup.dkim
      vars:
        dkim_domains:
          - domain: example.com
            selector: mail
            key_size: 2048
          - domain: example.org
            selector: default
            key_size: 2048
```

### With Rspamd

```yaml
- hosts: mail_servers
  roles:
    - role: alphanodes.setup.dkim
      vars:
        dkim_user: _rspamd
        dkim_group: _rspamd
        dkim_domains:
          - domain: example.com
            selector: mail

    - role: alphanodes.setup.rspamd
      vars:
        rspamd_dkim_selector: mail
        rspamd_dkim_key: /var/lib/dkim/example.com/mail.key
```

## Directory Structure

After running the role, keys are organized as:

```text
/var/lib/dkim/
├── example.com/
│   ├── mail.key          # Private key (0640, owner: dkim_user)
│   └── mail.txt          # Public key DNS record
└── example.org/
    ├── default.key
    └── default.txt
```

## DNS Configuration

After running the role, add the TXT record from the `.txt` file to your DNS:

```bash
# Display the DNS record
cat /var/lib/dkim/example.com/mail.txt

# Verify DNS propagation
dig +short TXT mail._domainkey.example.com
```

## Key Rotation

To rotate DKIM keys:

1. Set `dkim_force_regenerate: true`
2. Run the playbook
3. Update DNS records
4. Wait for DNS propagation (24-48 hours)
5. Set `dkim_force_regenerate: false`

**Important**: Keep old keys active during DNS TTL period!

## Security Considerations

- Private keys are stored with mode `0640` by default
- Keys are owned by the specified `dkim_user:dkim_group`
- Public keys (`.txt` files) are world-readable for easy access
- Never commit private keys to version control
- Use strong key sizes (2048+ bits)

## Testing

Run Molecule tests:

```bash
molecule test -s dkim
```

## License

MIT

## Author

AlphaNodes
