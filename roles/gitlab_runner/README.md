# Ansible Role: gitlab_runner

An Ansible Role that installs [GitLab Runner](https://docs.gitlab.com/runner/) with optional Hetzner Cloud Fleeting Plugin support on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        gitlab_runner_coordinator_url: https://gitlab.example.com
        gitlab_runner_concurrent: 10

      roles:
        - alphanodes.setup.gitlab_runner
```

## Runner Configuration

The role does not generate `config.toml` itself. It only deploys a host specific template, if one exists in the playbook directory:

```text
{{ playbook_dir }}/files/gitlab-runner/{{ inventory_hostname }}.toml.j2
```

## Hetzner Cloud Fleeting Plugin

With `gitlab_runner_with_hetzner_fleed: true` (default) the Hetzner Fleeting Plugin is installed for autoscaling runners in Hetzner Cloud. The plugin itself is configured in the `config.toml` template, which can use the `gitlab_runner_hetzner_*` variables.
