# Ansible Role: vimbadmin

An Ansible Role that installs [ViMbAdmin](https://www.vimbadmin.net/) for managing mail domains, mailboxes and aliases on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        vimbadmin_vhost_server: mailconfig.example.com
        vimbadmin_securitysalt: "{{ vault_vimbadmin_securitysalt }}"
        vimbadmin_rememberme_salt: "{{ vault_vimbadmin_rememberme_salt }}"
        vimbadmin_password_salt: "{{ vault_vimbadmin_password_salt }}"

      roles:
        - alphanodes.setup.vimbadmin
```

The three salt variables have no defaults and must be unique random strings, keep them in Ansible Vault.
