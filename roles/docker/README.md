# Role: docker

Installs Docker CE from the official Docker repository.

## Supported Platforms

- Debian (bookworm, trixie)
- Ubuntu (noble)

## Dependencies

- `alphanodes.setup.common`

## Variables

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `docker_version` | `''` | Pin docker-ce to a version, e.g. `5:29.6.2`. Empty installs the latest |
| `docker_versioned_packages` | `[docker-ce, docker-ce-cli]` | Packages that follow `docker_version` |
| `docker_with_compose` | `false` | Install docker-compose standalone binary |
| `docker_compose_version` | `2.40.3` | Version of docker-compose to install |
| `docker_remove` | `false` | Remove Docker instead of installing |

See `defaults/main.yml` for all configurable options.

## Example Usage

```yaml
- hosts: servers
  roles:
    - role: alphanodes.setup.docker
      vars:
        docker_with_compose: true
```

## Notes

- Uses official Docker CE repository (not Debian/Ubuntu packages)
- Removes legacy docker packages before installation
- Docker-compose is installed as standalone binary to `/usr/local/bin/docker-compose`
- A set `docker_version` also puts the affected packages on hold, so a later
  `apt dist-upgrade` cannot move them. Downgrades are allowed, so lowering the
  version is enough to roll back. Clearing the variable releases the hold again
