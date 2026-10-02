# Ansible Role: zsh

An Ansible Role that installs [zsh](https://www.zsh.org/) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.zsh
```

## Prompt

The prompt uses [starship](https://starship.rs) with Nerd Font symbols, so the terminal on the client needs a [Nerd Font](https://www.nerdfonts.com). Leftovers of the former powerlevel10k setup (cache files, `/usr/share/powerlevel10k`) are removed automatically, the directory as soon as no `.zshrc` on the host uses it anymore.
