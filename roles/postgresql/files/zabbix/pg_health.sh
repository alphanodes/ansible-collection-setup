#!/bin/sh
# Server and database state that the agent 2 plugin does not report, as JSON
# for the Zabbix UserParameter pg_health (through sudo as postgres, as
# pg_file_settings needs a superuser). Mostly signs of a configuration the
# role rendered wrong or that did not take effect.
# Root owned, so zabbix cannot change what runs as postgres.
set -eu

q() {
  psql -X -t -A "$@"
}

# Separate assignments, so set -e stops on a failing psql. Inside a command
# substitution of printf or the for list a failure would be ignored and the
# check would report 0.
# A changed setting that needs a restart is listed as an error as well, it
# is counted by pending_restart
config_errors=$(q -c "SELECT count(*) FROM pg_file_settings f WHERE error IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pg_settings s WHERE s.name = f.name AND s.pending_restart)")
pending_restart=$(q -c "SELECT count(*) FROM pg_settings WHERE pending_restart")
inactive_slots=$(q -c "SELECT count(*) FROM pg_replication_slots WHERE NOT active")
# WAL that the slots keep on disk, a standby has no current WAL position
slot_retained_bytes=$(q -c "SELECT CASE WHEN pg_is_in_recovery() THEN 0 ELSE coalesce(max(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)), 0)::bigint END FROM pg_replication_slots")
autovacuum_max_workers=$(q -c "SELECT current_setting('autovacuum_max_workers')")

dbs=$(q -c "SELECT datname FROM pg_database WHERE datallowconn AND datname !~ '[[:space:]]'")
invalid_indexes=0
timescaledb_failed_jobs=0
for db in $dbs; do
  # Left behind by a failed CREATE INDEX CONCURRENTLY or REINDEX CONCURRENTLY
  row=$(q -F ' ' -d "$db" -c "SELECT (SELECT count(*) FROM pg_index WHERE NOT indisvalid), (SELECT count(*) FROM pg_extension WHERE extname = 'timescaledb')")
  invalid_indexes=$((invalid_indexes + ${row% *}))
  if [ "${row#* }" -gt 0 ]; then
    failed=$(q -d "$db" -c "SELECT count(*) FROM timescaledb_information.job_stats WHERE last_run_status = 'Failed'")
    timescaledb_failed_jobs=$((timescaledb_failed_jobs + failed))
  fi
done

printf '{"config_errors":%s,"pending_restart":%s,"inactive_slots":%s,"slot_retained_bytes":%s,"autovacuum_max_workers":%s,"invalid_indexes":%s,"timescaledb_failed_jobs":%s}\n' \
  "$config_errors" "$pending_restart" "$inactive_slots" "$slot_retained_bytes" \
  "$autovacuum_max_workers" "$invalid_indexes" "$timescaledb_failed_jobs"
