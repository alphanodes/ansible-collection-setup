# Ansible Role: ssh server

Run ssh server and manage ssh keys (private keys), authorized_keys and known_hosts files of users.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
ssh_server_packages:
  - openssh-server
```

Debian packages, which should be installed.

```yaml
ssh_server_include_sshd_config_d: false
```

If true, /etc/ssh/sshd_config.d/*.conf is included and allows overwrite settings.

```yaml
ssh_server_port: 22
```

The port on which sshd will listen for requests.

```yaml
ssh_server_password_authentication: false
```

Whether to accept passwords for authentication.

```yaml
ssh_server_challenge_response_authentication: false
```

Whether challenge-response passwords should be used or not.

```yaml
ssh_server_use_pam: true
```

Whether PAM authentication should be used or not.

```yaml
ssh_server_permit_root_login: without-password
```

Should root login be allowed? Possible values are: without-password, 'yes' or 'no'

```yaml
ssh_server_recreate_host_keys: false
```

`ssh_server_recreate_host_keys` to yes will recreate host keys. Most likely you to not want to set it to
yes permanently.

```yaml
ssh_server_hostkeys:
  - /etc/ssh/ssh_host_ed25519_key
  - /etc/ssh/ssh_host_rsa_key
  - /etc/ssh/ssh_host_ecdsa_key
```

Available host keys for ssh server.

```yaml
ssh_server_match_group: []
```

Introduces a conditional block.  If all of the criteria on the Match line are satisfied, the keywords on the following lines override those set in the global section of the config

```yaml
ssh_server_match_user: []
```

Introduces a conditional block.  If all of the criteria on the Match line are satisfied, the keywords on the following lines override those set in the global section of the config file, until either another Match line or the end of the file.

```yaml
ssh_max_secure: true
```

if `ssh_max_secure` is yes, `KexAlgorithms`, `Ciphers` and `MACs` are set for ssh server. If set to no, these
options will not be set and default values of your ssh server will be used.

```yaml
ssh_key_algorithm: rsa
```

`ssh_key_algorithm` is used as default algorithm for ssh user keys (file name: id_ + `ssh_key_algorithm`). Choose between: rsa, dsa, ecdsa and ed25519. See https://www.ssh.com/ssh/keygen/ for more information.

```yaml
ssh_key_management_exclusive: true
```

Default settings for user, if keys are managned exclusive

```yaml
ssh_client_hash_known_hosts: true
```

ssh client configuration whether to use hashes for hostnames in known_hosts file or not. See https://www.ssh.com/ssh/config/ and https://security.stackexchange.com/questions/56268/ssh-benefits-of-using-hashed-known-hosts for more information.

```yaml
ssh_groups: []
```

System user groups, which should be created. This has nothing to do with ssh by itself, but sometimes you want create your own groups for ssh users, which should be used.

```yaml
ssh_management_access: []
```

`ssh_management_access` are public keys, which are added to `authorized_keys` if `with_management_access` is true.
For managing users (root or ansible_user) the default value is true for `with_management_access`. For all other users default value is false. You can overwride this for each user with `with_management_access`

```yaml
ssh_users: []
```

Users which should be configured for use with ssh. With `access` you can define a list of public keys, which are added to `authorized_keys`. `with_management_access` use can configure, if `ssh_management_access` should be added to `authorized_keys`, too. With `private_keys` you can specify a list of private ssh keys, which should be added.

```yaml
ssh_known_hosts: []
```

List of known_hosts, which should be added to `known_hosts` file of all users. Use `ssh-keyscan -t ed25519,rsa,ecdsa HOST` to create key entries. Use can overwrite `ssh_known_hosts` for each user with `known_hosts`.

```yaml
ssh_all_known_hosts: []
```

Same as `ssh_known_hosts`, but you **cannot** overwrite it user based with `known_hosts`.

## Example Playbook with just ssh server

```yaml
- hosts: all

  roles:
    - alphanodes.setup.ssh
```

## Example Playbook with key management

```yaml
- hosts: all

  vars:
    # used for all users as default
    ssh_known_hosts:
      - name: myhost.com
        key: 'myhost.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIO1TMULuqiGtbwkbbPccedorx7jqlrDyRCHg3978a7iy'
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
          - name: myhost1.com
            key: 'myhost1.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIO1TMULuqiGtbwkbbPccedorx7jqlrDyRCHg3978a7iy'

  roles:
    - alphanodes.setup.ssh
```
