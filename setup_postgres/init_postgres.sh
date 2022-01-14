#!/bin/bash
set -eux

THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# PostgreSQL database initialisation
psql postgres -c "CREATE USER youruser PASSWORD 'yourpassword'"
# the -O flag below sets the user: createdb -O DBUSER DBNAME
createdb -O youruser virtualbank
