# Role: gitlab_runner

Installs GitLab Runner from the official GitLab repository with optional Hetzner Cloud Fleeting Plugin support.

## Supported Platforms

- Debian (bookworm, trixie)
- Ubuntu (noble)

## Dependencies

- `alphanodes.setup.common`
- `alphanodes.setup.docker`

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `gitlab_runner_coordinator_url` | `''` | GitLab server URL |
| `gitlab_runner_with_hetzner_fleed` | `true` | Install Hetzner Fleeting Plugin |
| `gitlab_runner_concurrent` | `{{ ansible_processor_nproc }}` | Max concurrent jobs |
| `gitlab_runner_apt_pinning` | `false` | Pin GitLab repository packages |
| `gitlab_runner_remove` | `false` | Remove GitLab Runner instead of installing |

See `defaults/main.yml` for all configurable options including Hetzner Cloud settings.

## Configuration

The role looks for a host-specific config.toml template at:

```text
{{ playbook_dir }}/files/gitlab-runner/{{ inventory_hostname }}.toml.j2
```

## Example Usage

```yaml
- hosts: runners
  roles:
    - role: alphanodes.setup.gitlab_runner
      vars:
        gitlab_runner_coordinator_url: https://gitlab.example.com
        gitlab_runner_concurrent: 10
```

## Hetzner Cloud Fleeting Plugin

When `gitlab_runner_with_hetzner_fleed: true`, the Hetzner Fleeting Plugin is installed for autoscaling runners in Hetzner Cloud.

Key variables:

- `gitlab_runner_hetzner_server_location`: Hetzner datacenter (default: `nbg1`)
- `gitlab_runner_hetzner_server_type`: Server type (default: `cx23`)
- `gitlab_runner_hetzner_image`: OS image (default: `debian-13`)
- `gitlab_runner_hetzner_api_token`: Hetzner Cloud API token

## Notes

- Uses official GitLab Runner repository
- Configures systemd service with graceful shutdown (720s timeout)
- Removes bash_logout to prevent logout issues
