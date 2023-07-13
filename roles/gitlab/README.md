# Ansible Role: gitlab

Setup [GitLab source installation](https://docs.gitlab.com/ee/install/installation.html) (without docker)

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        gitlab_root_password: yourdefaultpassword

      roles:
        - alphanodes.setup.gitlab
```
