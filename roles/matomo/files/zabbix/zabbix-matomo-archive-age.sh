#!/bin/bash
# Returns the age in seconds of the LastCompletedFullArchiving option
# (UNIX_TIMESTAMP() - option_value) from the Matomo MySQL database.
#
# Used by the Zabbix agent 2 UserParameter matomo.archive.last_success.age.
# Outputs a single integer on stdout, or nothing if the value cannot be read
# (Zabbix interprets empty output as ZBX_NOTSUPPORTED).
set -u

CNF=${MATOMO_ZABBIX_CNF:-/etc/zabbix/matomo.my.cnf}

if [[ ! -r $CNF ]]; then
    exit 0
fi

mysql --defaults-extra-file="$CNF" -N -B -e \
    "SELECT UNIX_TIMESTAMP() - option_value FROM matomo.piwik_option WHERE option_name = 'LastCompletedFullArchiving';" \
    2>/dev/null
