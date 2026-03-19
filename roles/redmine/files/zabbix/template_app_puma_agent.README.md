# Puma (Zabbix Template)

## Overview

Performance monitoring for Puma web server using pumactl stats via the Puma
control socket. Collects worker, thread and request metrics through a Zabbix
agent UserParameter without impacting application performance.

Designed for Puma running in cluster mode (multiple workers) but also supports
single mode. All metrics are extracted from a single `pumactl stats` JSON
response using dependent items with JavaScript preprocessing.

## Requirements

Zabbix version: 7.4 and higher.

### Prerequisites

- Zabbix agent with **UserParameter `puma_stats`** configured
- sudo access for `zabbix` user to run `pumactl` as the application user
- Puma **control app enabled** (`activate_control_app` in puma.rb)
- Puma **state file** at `/run/<instance>/redmine.state`

### Permissions

The `zabbix` user needs sudo access to the application user. The Redmine
Ansible role configures this automatically:

```text
zabbix ALL = (<redmine_user>) NOPASSWD: ALL
```

The UserParameter command runs:

```bash
sudo -u <instance> -i -- pumactl stats -S /run/<instance>/redmine.state
```

## Tested versions

This template has been tested on:

- Puma 6.x with Redmine 6.0/6.1

## Configuration

The Zabbix agent must have the `puma_stats` UserParameter configured. This
is handled automatically by the `zabbix_agent` Ansible role when
`redmine_instances` is defined.

### Macros used

| Name | Description | Default |
| ---- | ----------- | ------- |
| {$PUMA.INSTANCE} | Instance name (system user and run directory) | `redmine` |
| {$PUMA.UPDATE.INTERVAL} | Stats collection interval | `30s` |
| {$PUMA.BACKLOG.HIGH} | Critical backlog threshold | `5` |
| {$PUMA.UTILIZATION.WARN} | Warning utilization percentage | `80` |
| {$PUMA.UTILIZATION.HIGH} | Critical utilization percentage | `95` |
| {$PUMA.NODATA.TIMEOUT} | Timeout for missing data alert | `5m` |

### Items

| Name | Type | Description |
| ---- | ---- | ----------- |
| Puma: Get stats | Active (master) | Raw JSON from pumactl stats |
| Puma: Workers configured | Dependent | Number of configured worker processes |
| Puma: Workers booted | Dependent | Number of currently booted workers |
| Puma: Old workers | Dependent | Workers pending shutdown during restart |
| Puma: Total backlog | Dependent | Requests waiting for a free thread |
| Puma: Pool capacity | Dependent | Idle threads available for requests |
| Puma: Running threads | Dependent | Total spawned threads (busy + idle) |
| Puma: Max threads | Dependent | Total thread capacity (workers x max_threads) |
| Puma: Total requests | Dependent | Cumulative requests served (counter) |
| Puma: Requests per second | Dependent | Request rate (change per second) |
| Puma: Thread utilization | Dependent | Percentage of thread capacity in use |

### Triggers

| Name | Severity | Description |
| ---- | -------- | ----------- |
| No stats data received | HIGH | Puma may be down or UserParameter misconfigured |
| Workers not fully booted | WARNING | Not all workers are running (crash or boot failure) |
| Old workers present | INFO | Stuck phased restart (old workers for > 10 min) |
| Request backlog detected | WARNING | Sustained backlog for > 5 min (all threads busy) |
| High request backlog | HIGH | Backlog exceeds critical threshold |
| High thread utilization | WARNING | Average utilization > 80% over 5 min |
| Critical thread utilization | HIGH | Average utilization > 95% over 5 min |

### Graphs

| Name | Description |
| ---- | ----------- |
| Puma: Thread utilization | Utilization percentage over time (gradient). The key graph for capacity planning. |
| Puma: Thread pool | Max threads (ceiling), running threads, and pool capacity overlaid. Shows thread saturation at a glance. |
| Puma: Requests per second | Throughput over time (gradient). Correlate with utilization to find bottlenecks. |
| Puma: Request backlog | Queued requests over time. Should normally be flat at zero — any spike means saturation. |
| Puma: Workers | Configured, booted, and old workers. Divergence indicates crashes or stuck restarts. |

### Key metrics explained

**Backlog** is the most important metric. A non-zero backlog means all threads
are busy and requests are waiting. Sustained backlog indicates the server needs
more workers or threads.

**Thread utilization** shows what percentage of the total thread pool is busy.
Calculated as `(1 - pool_capacity / max_threads) × 100`. Values consistently
above 80% suggest the server is approaching saturation.

**Pool capacity** shows how many threads are immediately available. When this
drops to 0, requests start queuing in the backlog.

### Interpreting the data

| Question | Metric | Signal |
| -------- | ------ | ------ |
| Server oversized? | Pool capacity ≈ max threads, utilization < 20% | Too many workers |
| Server idle? | Backlog = 0, requests/s low, utilization < 10% | Underutilized |
| Under load? | Backlog > 0, pool capacity = 0 | Workers saturated |
| Why slow? | Running threads high, backlog growing | Need more workers/threads |

### Multiple instances

For hosts with multiple Redmine instances, link the template once per instance
and override the `{$PUMA.INSTANCE}` macro at the host level for each link.
