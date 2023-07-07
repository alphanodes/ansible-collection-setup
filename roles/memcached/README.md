# Ansible Role: Memcached

An Ansible Role that installs Memcached on Debian/Ubuntu Linux.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    memcached_user: memcache

The user under which the Memcached daemon will run.

    memcached_port: 11211
    memcached_listen_ip: 127.0.0.1

The port and IP address (127.0.0.1 for localhost) on which Memcached will listen for requests.

    memcached_threads: 4

Number of threads to run.

    memcached_memory_limit: 64
    memcached_max_item_size: 1m
    memcached_connections: 1024

Memcached limits. The maximum amount of RAM `memcached` will consume (64MB is the default), the memory-limit of a single item and the maximum number of simultaneous connections memcached will handle.

    memcached_log_file: /var/log/memcached.log

The location of the memcached log file.

    memcached_log_verbosity: ""

Normally memcached does not log anything. Change to "-v" to enable logging or to "-vv" for debug logging.

## Dependencies

None.

## Example Playbook

    - hosts: cache
      roles:
        - { role: alphanodes.setup.memcached }
