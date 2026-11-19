# Ansible Role: pandoc

An Ansible Role that installs the document converter [Pandoc](https://pandoc.org/) from the upstream Debian package on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.pandoc
```

The upstream package replaces a `pandoc` package of the distribution, which is too old for some input formats (e.g. xlsx).
