# GitLab (Zabbix Template)

## Overview

Log-based error monitoring for GitLab Omnibus installations using native
Zabbix `log[]` and `log.count[]` active check items, plus a readiness check
of all GitLab components.

This template monitors GitLab Omnibus log files directly via the Zabbix
agent, detecting errors in nginx, Puma, Sidekiq and Gitaly without
requiring the Prometheus metrics endpoint.

Can be combined with the "GitLab by HTTP" template for performance
metrics via `/-/metrics` (requires `gitlab_prometheus_enable: true`).

## Requirements

Zabbix version: 7.4 and higher.

### Prerequisites

- Zabbix agent with **active checks** enabled (`ServerActive` configured)
- Read access to `/var/log/gitlab/` for the Zabbix user
- GitLab Omnibus installation with default log paths
- UserParameter `gitlab.readiness`, deployed by the `alphanodes.setup.gitlab_omnibus`
  role. It queries `/-/readiness?all=1` on 127.0.0.1, which is always part of
  `gitlab_monitoring_ip_whitelist`

### File permissions

The monitored log files must be readable by the `zabbix` user. On a
default GitLab Omnibus installation, the following files are
world-readable (644):

| File | Owner | Permissions |
| ---- | ----- | ----------- |
| `/var/log/gitlab/nginx/gitlab_error.log` | root:root | 644 |
| `/var/log/gitlab/puma/puma_stderr.log` | git:git | 644 |
| `/var/log/gitlab/sidekiq/current` | root:root | 644 |
| `/var/log/gitlab/gitaly/current` | root:root | 644 |

## Tested versions

This template has been tested on:

- GitLab Omnibus 18.9.2 EE

## Configuration

No special agent configuration required beyond the standard `ServerActive`
setting. All monitoring logic is contained in this template.

### Macros used

| Name | Description | Default |
| ---- | ----------- | ------- |
| {$GITLAB.NGINX.ERROR.LOG} | Path to nginx error log | `/var/log/gitlab/nginx/gitlab_error.log` |
| {$GITLAB.PUMA.ERROR.LOG} | Path to Puma stderr log | `/var/log/gitlab/puma/puma_stderr.log` |
| {$GITLAB.SIDEKIQ.LOG} | Path to Sidekiq log | `/var/log/gitlab/sidekiq/current` |
| {$GITLAB.GITALY.LOG} | Path to Gitaly log | `/var/log/gitlab/gitaly/current` |
| {$GITLAB.NGINX.CRIT.MAX} | Max critical nginx errors per interval | `0` |
| {$GITLAB.SIDEKIQ.FAIL.MAX} | Max Sidekiq failures per interval | `50` |
| {$GITLAB.GITALY.ERROR.MAX} | Max Gitaly errors per interval | `10` |
| {$GITLAB.LOG.MAXDELAY} | Max delay for log processing (seconds) | `60` |
| {$GITLAB.NODATA.TIMEOUT} | Nodata timeout for log items | `30m` |
| {$GITLAB.SIDEKIQ.EVAL.PERIOD} | Evaluation period for Sidekiq trigger | `15m` |
| {$GITLAB.GITALY.EVAL.PERIOD} | Evaluation period for Gitaly trigger | `15m` |

### Items

| Name | Type | Key | Description |
| ---- | ---- | --- | ----------- |
| nginx: Error log | Log (active) | `log[...]` | Captures error/crit/alert/emerg nginx entries |
| nginx: Critical error count | Numeric (active) | `log.count[...]` | Count of crit/alert/emerg entries per interval |
| Puma: Error log | Log (active) | `log[...]` | Captures Puma application errors and OOM events |
| Puma: Error count | Numeric (active) | `log.count[...]` | Count of fatal/OOM errors per interval |
| Sidekiq: Failure count | Numeric (active) | `log.count[...]` | Count of failed background jobs per interval |
| Gitaly: Error count | Numeric (active) | `log.count[...]` | Count of Gitaly error/fatal entries per interval |
| GitLab: Readiness | Text (active) | `gitlab.readiness` | Raw readiness JSON, not stored |
| GitLab: Readiness status | Dependent | `gitlab.readiness.status` | ok, failed or unreachable |

### Triggers

| Name | Severity | Description |
| ---- | -------- | ----------- |
| nginx file descriptor exhaustion | HIGH | Detects "Too many open files" errors |
| nginx critical errors detected | WARNING | Critical nginx errors in every check for 5 minutes (short restarts are ignored) |
| Puma application errors detected | WARNING | Fatal errors, OOM kills in Puma |
| High Sidekiq job failure rate | WARNING | Sidekiq failure count exceeds threshold |
| High Gitaly error rate | WARNING | Gitaly error count exceeds threshold |
| Not ready | HIGH | Readiness not ok for 5 checks in a row (short restarts are ignored) |
| No readiness data | WARNING | No readiness data for `{$GITLAB.NODATA.TIMEOUT}` |

### Graphs

| Name | Description |
| ---- | ----------- |
| GitLab: Error rates by component | All 4 error counts (nginx, Puma, Sidekiq, Gitaly) overlaid. Shows at a glance which component is producing errors. |

### Noise filtering

The Puma error log item filters out known non-critical warnings:

- PostgreSQL collation version mismatch warnings
- BatchLoader deprecation warnings
- GraphQL-Ruby deprecation warnings

### Combining with GitLab by HTTP

For comprehensive monitoring, combine this template with "GitLab by HTTP":

- **GitLab** (this template): Error detection from log files. Works
  without Prometheus.
- **GitLab by HTTP**: Performance metrics (Puma utilization, Redis,
  DB connections). Requires `gitlab_prometheus_enable: true`.
