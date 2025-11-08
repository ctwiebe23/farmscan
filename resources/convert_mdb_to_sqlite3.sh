#!/bin/bash

# based on <https://acaird.github.io/2025/06/12/convert-msaccess-mdb-to-sqlite>

CMDFILE=sqlitecmds.txt
MDBFILE=./soildb_NE_2003.mdb
SQLFILE=./database.db

mdb-schema \
    "$MDBFILE" | \
    sed -E 's/(\]|\[)/`/g' | \
    sed '/CREATE TABLE MSysCompactError/,+6d' | \
    sed 's$Memo\/Hyperlink$Text$' \
    > schema.txt

[ ! -f "$SQLFILE" ] || rm "$SQLFILE"
sqlite3 "$SQLFILE" < schema.txt

TABLES=$(
    mdb-tables -d "," "$MDBFILE" | \
        sed "s/ /_/g" | \
        sed 's/MSysCompactError //' | \
        sed "s/,/ /g"
)

[ -d ./csv ] || mkdir ./csv

echo ".mode csv" > "$CMDFILE"

for table in $TABLES; do
    SQLTABLE="\"${table//_/ }\""
    echo "exporting table: $table / $SQLTABLE"
    mdb-export  "$MDBFILE" "${SQLTABLE//\"/}" > "./csv/${table}.csv"
    echo "delete from $SQLTABLE;" >> "$CMDFILE"
    echo .import --skip 1 "./csv/${table}.csv" "$SQLTABLE" >> "$CMDFILE"
    echo "exported table: $table / $SQLTABLE"
done
echo "importing tables into SQLite"
sqlite3 database.db < "$CMDFILE"
