# Ansible Role: dendrite

An Ansible Role that installs the [Matrix Dendrite](https://github.com/matrix-org/dendrite) homeserver on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        dendrite_server_name: matrix.example.com

      roles:
        - alphanodes.setup.dendrite
```

## Matrix Room Cleaner

With `dendrite_with_matrix_room_cleaner: true` the role builds a small Go helper and runs it weekly via the `matrix-room-cleaner.timer`. It prunes events older than `dendrite_cleaner_matrix_max_age_days` from the room `dendrite_cleaner_matrix_room_id`. The access token needs permission to redact messages in that room.

For a one-off run without the timer, call the binary with the environment it expects:

```bash
MATRIX_BASE=https://matrix.example.com MATRIX_TOKEN=YOUR_TOKEN ROOM_ID='!abc123:example.com' MAX_AGE_DAYS=7 /usr/local/bin/matrix_room_cleaner
```
