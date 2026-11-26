# Ansible Role: matrix_room_cleaner

An Ansible Role that redacts events older than a given number of days in one Matrix room, weekly via a systemd timer.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        matrix_room_cleaner_base: https://matrix.example.com
        matrix_room_cleaner_token: YOUR_TOKEN
        matrix_room_cleaner_room_id: '!abc123:example.com'

      roles:
        - alphanodes.setup.matrix_room_cleaner
```

## Access Token

The token belongs to a bot user that is a member of the room with permission to redact messages of others (moderator, power level 50). The cleaner only uses the client-server API, so it works with any homeserver.

For a one-off run without the timer, call the binary with the environment it expects:

```bash
MATRIX_BASE=https://matrix.example.com MATRIX_TOKEN=YOUR_TOKEN ROOM_ID='!abc123:example.com' MAX_AGE_DAYS=7 /usr/local/bin/matrix_room_cleaner
```
