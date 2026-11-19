-- Databases whose collation version differs from the one of the operating
-- system (glibc/ICU update), used by the Zabbix UserParameter
-- pg_collation_mismatch through sudo as postgres
SELECT count(*) FROM pg_database WHERE datcollversion <> pg_database_collation_actual_version(oid);
