#!/bin/sh
# Number of installed extensions in all databases whose version is older than
# the one of the installed package (ALTER EXTENSION ... UPDATE missing), used
# by the Zabbix UserParameter pg_extension_outdated through sudo as postgres.
# Root owned, so zabbix cannot change what runs as postgres.
set -eu

# A separate assignment, so set -e stops on a failing psql. Inside the for
# list a failure would be ignored and the check would report 0.
dbs=$(psql -X -t -A -c "SELECT datname FROM pg_database WHERE datallowconn AND datname !~ '[[:space:]]'")
total=0
for db in $dbs; do
  count=$(psql -X -t -A -d "$db" -c "SELECT count(*) FROM pg_available_extensions WHERE installed_version IS NOT NULL AND installed_version <> default_version")
  total=$((total + count))
done
echo "$total"
