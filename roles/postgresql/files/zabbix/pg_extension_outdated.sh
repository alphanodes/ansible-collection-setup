#!/bin/sh
# Number of installed extensions in all databases whose version is older than
# the one of the installed package (ALTER EXTENSION ... UPDATE missing), used
# by the Zabbix UserParameter pg_extension_outdated through sudo as postgres.
# Root owned, so zabbix cannot change what runs as postgres.
set -eu

total=0
for db in $(psql -X -t -A -c "SELECT datname FROM pg_database WHERE datallowconn AND datname !~ '[[:space:]]'"); do
  count=$(psql -X -t -A -d "$db" -c "SELECT count(*) FROM pg_available_extensions WHERE installed_version IS NOT NULL AND installed_version <> default_version")
  total=$((total + count))
done
echo "$total"
