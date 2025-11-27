# Role: alloy

Installs and configures Grafana Alloy for log shipping to Loki.

## Supported platforms

- Debian 12/13
- Ubuntu 24.04

## Dependencies

- alphanodes.setup.common

## Variables

See `defaults/main.yml` for all configurable options. Key variables:

- `alloy_loki_url` - Loki endpoint URL
- `alloy_basic_user` / `alloy_basic_pass` - Authentication credentials
- `alloy_with_postgres` - Enable PostgreSQL log collection
- `alloy_with_redmine` - Enable Redmine log collection
- `alloy_drop_*_regex` - Noise filter patterns
