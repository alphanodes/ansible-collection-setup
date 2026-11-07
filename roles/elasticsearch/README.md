# Ansible Role: elasticsearch

An Ansible Role that installs a local single-node [Elasticsearch](https://www.elastic.co/elasticsearch) service on Debian 13 and Ubuntu 26.04 from official Debian packages.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml).

## Example Playbook

```yaml
- hosts: all
  roles:
    - alphanodes.setup.elasticsearch
```

## Local Service

This role provides an unauthenticated search endpoint exclusively on loopback, intended for applications on the same trusted host. It does not support remote access, clusters or adopting an existing secured Elasticsearch installation. For these deployments, manage Elasticsearch separately and configure the consuming application with its endpoint and credentials.

Elasticsearch includes its own Java runtime. An empty package version installs the repository candidate without upgrading existing installations; pin an exact version to request a controlled upgrade.

Set `elasticsearch_enabled: false` to install the package while keeping its service stopped, disabled and masked. This mode satisfies package dependencies without starting a JVM or changing the host sysctl. Setting it back to true removes the mask and starts the service.
