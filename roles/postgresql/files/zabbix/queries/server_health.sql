-- Server state that the plugin keys do not report, one row for the template
-- PostgreSQL Custom (pgsql.custom.query with the database of {$PG.DATABASE}).
-- Mostly signs of a configuration the role rendered wrong or that did not
-- take effect. pg_file_settings needs the grants of the postgresql role.
SELECT
  -- A changed setting that needs a restart is listed as an error as well,
  -- it is counted by pending_restart
  (SELECT count(*) FROM pg_file_settings f
    WHERE f.error IS NOT NULL
      AND NOT EXISTS (SELECT 1 FROM pg_settings s WHERE s.name = f.name AND s.pending_restart)) AS config_errors,
  (SELECT count(*) FROM pg_settings WHERE pending_restart) AS pending_restart,
  (SELECT count(*) FROM pg_replication_slots WHERE NOT active) AS inactive_slots,
  -- WAL that the slots keep on disk, a standby has no current WAL position
  CASE WHEN pg_is_in_recovery() THEN 0
    ELSE (SELECT coalesce(max(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)), 0)::bigint FROM pg_replication_slots)
  END AS slot_retained_bytes,
  current_setting('autovacuum_max_workers')::integer AS autovacuum_max_workers,
  -- glibc or ICU updated without ALTER DATABASE ... REFRESH COLLATION VERSION
  (SELECT count(*) FROM pg_database
    WHERE datcollversion <> pg_database_collation_actual_version(oid)) AS collation_mismatch
