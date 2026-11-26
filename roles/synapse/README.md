# Ansible Role: synapse

An Ansible Role that installs the Matrix homeserver [Synapse](https://github.com/element-hq/synapse) from the matrix.org packages with PostgreSQL and nginx on Debian and Ubuntu servers.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        synapse_server_name: matrix.example.com
        synapse_registration_shared_secret: YOUR_SECRET

      roles:
        - alphanodes.setup.synapse
```

With element-web at the root of the same vhost:

```yaml
    - hosts: all

      vars:
        synapse_server_name: matrix.example.com
        synapse_registration_shared_secret: YOUR_SECRET
        synapse_vhost_root: /usr/share/element-web
        element_web_with_vhost: false

      roles:
        - alphanodes.setup.synapse
        - alphanodes.setup.element_web
```

## Notes

- The matrix.org packages exist for amd64 only.
- `synapse_server_name` is part of every user and room ID. Changing it later means starting over with a new database.
- Element X needs Simplified Sliding Sync, which Synapse offers since 1.114. The role checks it after every rollout.
- Registration is closed. Create users on the server as root with `register_new_matrix_user -c /etc/matrix-synapse/conf.d/alphanodes.yaml -u USER http://127.0.0.1:8008`, add `-a` for an admin.
- Logs go to journald: `journalctl -u matrix-synapse`.
- `synapse_remove` keeps the PostgreSQL database, drop it by hand once it is no longer needed.
