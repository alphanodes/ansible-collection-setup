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

The template relies on a Zabbix agent 2 UserParameter. The matomo role
deploys the following files when `zabbix_monitoring` is enabled on the
DB host:

| File | Purpose |
| ---- | ------- |
| `/etc/zabbix/zabbix_agent2.d/matomo_archiver_userparameter.conf` | UserParameter definition |
| `/usr/local/bin/zabbix-matomo-archive-age.sh` | Helper script (mode 0755) |
| `/etc/zabbix/matomo.my.cnf` | MySQL credentials (mode 0640, owner zabbix:zabbix) |

A dedicated read-only MySQL user is required:

```sql
CREATE USER 'zabbix_monitor'@'localhost' IDENTIFIED BY '<secret>';
GRANT SELECT ON matomo.piwik_option TO 'zabbix_monitor'@'localhost';
FLUSH PRIVILEGES;
```

The credentials file uses the standard MySQL `[client]` format:

```ini
[client]
user=zabbix_monitor
password=<secret>
host=localhost
```

### Manual test on the monitored host

```bash
sudo -u zabbix /usr/local/bin/zabbix-matomo-archive-age.sh
# Expected: a single integer like 1234 (seconds since last successful run)
```

### Import into Zabbix

1. Zabbix UI -> Data collection -> Templates -> Import
2. Select `template_app_matomo_archiver.yaml`
3. Assign the template to the DB host in the host configuration
