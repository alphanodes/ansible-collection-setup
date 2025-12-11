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
| `docker_with_compose` | `false` | Install docker-compose standalone binary |
| `docker_compose_version` | `2.39.2` | Version of docker-compose to install |
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
