# Role: dendrite

Summary

- Installs and configures the Matrix Dendrite server on Debian/Ubuntu.

Supported platforms

- Debian, Ubuntu

Dependencies

- No external dependencies outside this collection.

Variables

- See `defaults/main.yml` and `vars/` for configurable options.

Notes

- Integrated and tested through service-specific playbooks/Molecule scenarios in this collection.

Matrix Room Cleaner

- Purpose: Periodically prune events older than a defined age from a specific Matrix room.
- Implementation: A small Go helper (`matrix_room_cleaner`) built on the target and executed via a systemd timer using `alphanodes.setup.systemd_timer`.

Parameters (defaults/main.yml)

- `dendrite_with_matrix_room_cleaner` (bool): Enables deployment of the cleaner (binary + timer). Default: `false`.
- `dendrite_cleaner_matrix_base` (string): Base URL of your homeserver (e.g. `https://matrix.example.org`). Used as `MATRIX_BASE`.
- `dendrite_cleaner_matrix_token` (string): Access token with permissions to manage messages in the target room. Used as `MATRIX_TOKEN`.
- `dendrite_cleaner_matrix_room_id` (string): Fully qualified room ID to clean (e.g. `!abc123:example.org`). Used as `ROOM_ID`.
- `dendrite_cleaner_matrix_max_age_days` (int): Max age in days; events older than this are removed. Used as `MAX_AGE_DAYS`.
- `dendrite_cleaner_src_dir` (path): Source directory where the Go program is placed, default `/usr/local/src/matrix_room_cleaner`.
- `dendrite_cleaner_bin` (path): Path to the compiled binary, default `/usr/local/bin/matrix_room_cleaner`.

Use with systemd timer (recommended)

- Set `dendrite_with_matrix_room_cleaner: true` and provide the variables above. The role will:
  - Place the Go source and build `{{ dendrite_cleaner_bin }}`.
  - Install and enable a systemd timer (`matrix-room-cleaner.timer`) that runs weekly.

Use without timer (one-off/manual)

- You can run the cleaner manually without relying on the timer:
  1) Ensure the binary exists (include the cleaner tasks once, or build from `roles/dendrite/files/matrix_room_cleaner.go`).
  2) Execute it with the required environment variables:
     - Example:
       - `MATRIX_BASE=https://matrix.example.org \
          MATRIX_TOKEN=YOUR_TOKEN \
          ROOM_ID=!abc123:example.org \
          MAX_AGE_DAYS=7 \
          {{ dendrite_cleaner_bin }}`
  3) Optional: Launch a one-shot run via systemd without installing a persistent timer:
     - `systemd-run --unit=matrix-room-cleaner-manual --property=Type=oneshot \
        env MATRIX_BASE=https://matrix.example.org \
        env MATRIX_TOKEN=YOUR_TOKEN \
        env ROOM_ID=!abc123:example.org \
        env MAX_AGE_DAYS=7 \
        {{ dendrite_cleaner_bin }}`

Disable or remove the timer

- To disable temporarily: `systemctl disable --now matrix-room-cleaner.timer`.
- To remove fully via Ansible: Use the role’s remove tasks (`dendrite_remove: true`) or include `alphanodes.setup.systemd_timer` with `timers.matrix_room_cleaner.state: absent`.
