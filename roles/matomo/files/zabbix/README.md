# Matomo (Zabbix Templates)

Zabbix 7.4 templates for monitoring AlphaNodes-managed Matomo
installations. Each template covers one functional aspect and is meant
to be stacked on hosts according to their role (archiver, tracker,
database). On all-in-one installations all templates run on the same
host.

## Templates in this directory

| File | Template | Description |
| ---- | -------- | ----------- |
| `template_app_matomo_archiver.yaml` | Matomo Archiver | Age of last successful `core:archive` run |
| `template_app_matomo_tracker.yaml` | Matomo Tracker | QueuedTracking backlog and worker timer state |
| `template_app_matomo_frontend.yaml` | Matomo Frontend | External HTTP availability check (Web Scenario) |

## Matomo Archiver

### Archiver: purpose

Detects when the `core:archive` cron job stops producing successful runs.
The template reads the `LastCompletedFullArchiving` option from the
Matomo database -- the same value the admin UI uses for its warning
banner -- and exposes its age in seconds as a Zabbix item.

### Archiver: host assignment

Assign to the host that runs the Matomo MySQL database (multi-host
cluster) or to the all-in-one Matomo host.

### Archiver: items and triggers

| Item | Key | Trigger |
| ---- | --- | ------- |
| Age of last successful archive run | `matomo.archive.last_success.age` | `> 4h` WARNING, `> 12h` HIGH, `> 24h` DISASTER |

Thresholds are controlled by macros `{$MATOMO.ARCHIVE.AGE.WARN}`,
`{$MATOMO.ARCHIVE.AGE.HIGH}` and `{$MATOMO.ARCHIVE.AGE.DISASTER}`.

### Archiver: prerequisites on the monitored host

The Zabbix agent UserParameter is deployed by the **`mysql` role**, not
the matomo role -- the check runs against the local MySQL instance and
reuses the existing `zbx_monitor` user and its my.cnf at
`{{ zabbix_agent_home }}/.my.cnf`. The query is inline in the
UserParameter (no wrapper script), following the same pattern as the
postgresql role.

Opt in by setting on the DB host:

```yaml
mysql_with_matomo_archiver_check: true
```

The mysql role then deploys:

| File | Purpose |
| ---- | ------- |
| `/etc/zabbix/zabbix_agent2.d/matomo_archiver.conf` | UserParameter definition |

Setting the flag back to `false` (or removing it) cleans the file up on
the next run.

### Archiver: manual test on the monitored host

```bash
sudo -u zabbix zabbix_agent2 -t matomo.archive.last_success.age
# Expected: matomo.archive.last_success.age  [s|1234]
```

## Matomo Tracker

### Tracker: purpose

Detects when the Matomo QueuedTracking pipeline gets behind or stops.
Two signals are exposed:

- `matomo.queue.total_size` -- sum of `LLEN` over all Redis keys
  matching `trackingQueueV1*`. Grows when the worker cannot drain the
  queue fast enough.
- `matomo.queue.worker_timer_state` -- output of
  `systemctl is-active matomo-queuedtracking.timer`. Anything other
  than `active` means no worker is scheduled.

### Tracker: host assignment

Assign to the host that handles tracking with the QueuedTracking
plugin: the tracker node in a cluster, or the all-in-one host in a
single-server setup. Requires `matomo_with_redis: true`.

### Tracker: items and triggers

| Item | Key | Trigger |
| ---- | --- | ------- |
| Tracking queue backlog | `matomo.queue.total_size` | `> 50k for 30 min` HIGH, `> 250k for 30 min` DISASTER |
| Queue worker timer state | `matomo.queue.worker_timer_state` | `<> "active"` for 2 checks HIGH |

Backlog thresholds via macros `{$MATOMO.QUEUE.SIZE.WARN}` (50000) and
`{$MATOMO.QUEUE.SIZE.DISASTER}` (250000 -- matches Matomo's own
`notify_queue_threshold_single_queue` default).

### Tracker: prerequisites on the monitored host

The Zabbix agent UserParameter is deployed by the **`matomo` role**
when:

```yaml
matomo_with_tracker_check: true
```

The role then deploys:

| File | Purpose |
| ---- | ------- |
| `/etc/zabbix/zabbix_agent2.d/matomo_tracker.conf` | Two inline-query UserParameters |

Setting the flag back to `false` (or removing it) cleans the file up
on the next run.

The UserParameters call `redis-cli` and `systemctl` directly as the
zabbix user; both work out of the box with the default redis_server
role (localhost, no auth) and unprivileged systemd queries.

### Tracker: manual test on the monitored host

```bash
sudo -u zabbix zabbix_agent2 -t matomo.queue.total_size
sudo -u zabbix zabbix_agent2 -t matomo.queue.worker_timer_state
# Expected: a numeric backlog and the string "active"
```

## Matomo Frontend

### Frontend: purpose

External HTTP availability check via a Zabbix Web Scenario. The
scenario runs from the Zabbix server itself (not from the monitored
host) and performs a single GET request against the URL defined in
`{$MATOMO.FRONTEND.URL}`. Fails on non-200, missing `<title>Matomo`,
or timeout.

### Frontend: host assignment

Assign to whichever host logically "owns" the public Matomo vhost.
For multi-host clusters this is the load balancer (e.g. `webfe1`),
for all-in-one installations it is the host itself.

### Frontend: items and triggers

| Item | Key | Trigger |
| ---- | --- | ------- |
| Frontend HTTP check | `web.test.fail[Matomo frontend availability]` | `> 0` HIGH |
| Frontend response time | `web.test.time[Matomo frontend availability,GET frontend,resp]` | `> 5s for 15 min` WARNING |

The response time threshold is controlled by macro
`{$MATOMO.FRONTEND.RESPTIME.WARN}` (default `5`).

### Frontend: required host_vars

The Web Scenario needs to know which URL to hit. Set the host-level
macro `MATOMO.FRONTEND.URL` to the public Matomo URL (with scheme
and trailing slash), e.g.:

```yaml
zabbix_link_templates:
  - …
  - Matomo Frontend

zabbix_macros:
  - macro_key: MATOMO.FRONTEND.URL
    macro_value: 'https://{{ matomo_vhost_main }}/'   # or matomo_vhost_server in single-host setups
```

No Ansible task is needed on the monitored host -- the check is
fully external.

### Frontend: manual test

From the Zabbix server (or any machine):

```bash
curl -sSI https://web-analytics.uni-muenchen.de/ | head -3
# Expected: HTTP/2 200
```

### Import into Zabbix

> **Heads-up:** The template must exist in Zabbix **before** the first
> Ansible rollout for any host that references it in
> `zabbix_link_templates`. Otherwise the `zabbix_agent` role's API task
> aborts with `Template not found: Matomo Archiver`.

Use the central playbook in ansible_sysconfig, which validates via
`configuration.importcompare` (real dry-run) and substitutes the
`__DATE__` placeholder in the template's `vendor.version` field:

```bash
cd ~/dev/ansible_sysconfig

# Dry-run (validate only)
ansible-playbook zabbix_template_import.yml

# Actually import / update
ansible-playbook zabbix_template_import.yml -e zabbix_template_import=true
```

Add new template files to the `zabbix_template_files` list inside the
playbook before the first run. After import the host assignment is
taken care of by Ansible via `zabbix_link_templates` in the host_vars.

### Template UUIDs (RFC 4122 v4)

All UUIDs in `template_app_matomo_archiver.yaml` must be valid UUIDv4
strings (hyphen-stripped). Zabbix rejects everything else with
`Invalid parameter "/1/uuid": UUIDv4 is expected.`

Generate fresh ones with:

```bash
python3 -c "import uuid; print(uuid.uuid4().hex)"
```
