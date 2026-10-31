# Ansible Role: ruby

Setup [Ruby](https://www.ruby-lang.org/) on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      roles:
        - alphanodes.setup.ruby
```

Compiled ruby with [ruby-build](https://github.com/rbenv/ruby-build) and YJIT, installed to `/opt/ruby/4.0.9`:

```yaml
    - hosts: all
      vars:
        ruby_source: ruby_build
        ruby_version: 4.0.9

      roles:
        - alphanodes.setup.ruby
```

The distribution ruby is removed and `ruby`, `gem`, `bundle` etc. are linked to `/usr/local/bin`. If another package depends on the distribution ruby, the role fails instead of removing it, see `ruby_remove_system_ruby`.

Switching back to `ruby_source: package` removes the compiled versions, the links and ruby-build, and installs the distribution ruby again. Packages installed for the build (e.g. `rustc`) are kept, because other software could depend on them.
