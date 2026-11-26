# Ansible Role: ssh

An Ansible Role that runs the ssh server and manages ssh keys, authorized_keys and known_hosts files of users on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.ssh
```

## sshd configuration

The role keeps `/etc/ssh/sshd_config` of the distribution and writes its settings to `/etc/ssh/sshd_config.d/10-alphanodes.conf`. A `sshd_config` written by former versions of this role is replaced by the distribution file once. Otherwise the role only makes sure that `sshd_config` includes `sshd_config.d` and sets no `Port`, so changes of others (e.g. Google OS Login, which adds lines at the top and the bottom on each boot) stay. sshd uses the first value it reads, so the drop-in wins against the rest of `sshd_config` and later drop-ins, but not against lines above the `Include`.

## Example Playbook with key management

```yaml
    - hosts: all

      vars:
        # used for all users as default
        ssh_known_hosts:
          - name: myhost.example.com
            key: 'myhost.example.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIO1TMULuqiGtbwkbbPccedorx7jqlrDyRCHg3978a7iy'
        ssh_users:
          - name: root
            access:
              - company_user1.pub
              - company_user2.pub
            with_management_access: false
            private_keys:
              - host: github.com
                user: git
                dir: company1
                source_dir: company1_company2
          - name: user3
            access:
              - company_user3.pub
            known_hosts:
              - name: myhost1.example.com
                key: 'myhost1.example.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIO1TMULuqiGtbwkbbPccedorx7jqlrDyRCHg3978a7iy'

      roles:
        - alphanodes.setup.ssh
```

`access` lists public keys for `authorized_keys`, `private_keys` deploys private keys for the user. `ssh_management_access` keys are added as well when `with_management_access` is true, which is the default for root and `ansible_user` only. A user specific `known_hosts` replaces `ssh_known_hosts`, while `ssh_all_known_hosts` is always added. Create key entries with `ssh-keyscan -t ed25519,rsa,ecdsa HOST`.
