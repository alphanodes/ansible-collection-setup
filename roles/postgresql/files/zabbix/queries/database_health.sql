-- State of one database, for the item prototypes of the template PostgreSQL
-- Custom (pgsql.custom.query with {#DBNAME} of the query databases).
SELECT
  -- Left behind by a failed CREATE INDEX CONCURRENTLY or REINDEX CONCURRENTLY
  (SELECT count(*) FROM pg_index WHERE NOT indisvalid) AS invalid_indexes,
  -- Package updated without ALTER EXTENSION ... UPDATE
  (SELECT count(*) FROM pg_available_extensions
    WHERE installed_version IS NOT NULL AND installed_version <> default_version) AS outdated_extensions,
  -- The view only exists with TimescaleDB, query_to_xml runs the query only
  -- then, a plain reference would fail in all other databases
  CASE WHEN to_regclass('timescaledb_information.job_stats') IS NULL THEN 0
    ELSE (xpath('/row/failed/text()', query_to_xml(
      'SELECT count(*) AS failed FROM timescaledb_information.job_stats WHERE last_run_status = ''Failed''',
      false, true, '')))[1]::text::integer
  END AS timescaledb_failed_jobs
