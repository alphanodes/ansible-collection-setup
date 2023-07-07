# Ansible Role: svnserve service

Run svnserve on Debian and Ubuntu servers.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
svn_server_packages:
  - subversion
```

Debian packages, which should be installed.

```yaml
svn_server_user: svn
```

svn-serve will be run under the `svn_server_user`.

```yaml
svn_server_group: svn
```

User group of `svn_server_user`.

```yaml
svn_server_home: /srv/svn
```

Home directory of `svn_server_user`.

```yaml
svn_server_repositories: /srv/svn/repositories
```

Directory for repositories (this should be within `svn_server_home` directory). In this directory all
repositories will be stored. Make sure you have enough disk space on used partition.

```yaml
svn_server_user_password:
```

If you want to login with `svn_server_user` you can set a password.

```yaml
svn_server_remove: false
```

To uninstall svnserve with all data, set `svn_server_remove` to true.

```yaml
svn_server_remove_packages: false
```

If you want to remove debian packages with  `svn_server_remove`, set `svn_server_remove_packages` to true.

## Example Playbook

```yaml
- hosts: localhost
  roles:
    - alphanodes.setup.svn
```
