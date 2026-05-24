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

Further templates (Matomo Tracker, Matomo Database) will follow.

## Matomo Archiver

### Purpose

Detects when the `core:archive` cron job stops producing successful runs.
The template reads the `LastCompletedFullArchiving` option from the
Matomo database -- the same value the admin UI uses for its warning
banner -- and exposes its age in seconds as a Zabbix item.

### Host assignment

Assign to the host that runs the Matomo MySQL database (multi-host
cluster) or to the all-in-one Matomo host.

### Items and triggers

| Item | Key | Trigger |
| ---- | --- | ------- |
| Age of last successful archive run | `matomo.archive.last_success.age` | `> 4h` WARNING, `> 12h` HIGH, `> 24h` DISASTER |

Thresholds are controlled by macros `{$MATOMO.ARCHIVE.AGE.WARN}`,
`{$MATOMO.ARCHIVE.AGE.HIGH}` and `{$MATOMO.ARCHIVE.AGE.DISASTER}`.

### Prerequisites on the monitored host

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

### Manual test on the monitored host

```bash
sudo -u zabbix zabbix_agent2 -t matomo.archive.last_success.age
# Expected: matomo.archive.last_success.age  [s|1234]
```

### Import into Zabbix

1. Zabbix UI -> Data collection -> Templates -> Import
2. Select `template_app_matomo_archiver.yaml`
3. Assign the template to the DB host in the host configuration
