#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 -d "${POSTGRES_DB}" -U "${POSTGRES_USER}" <<EOFSQL
    CREATE TABLE IF NOT EXISTS tournament (
        player VARCHAR (255) NOT NULL PRIMARY KEY,
        points INTEGER NOT NULL DEFAULT 0,
        since date DEFAULT CURRENT_TIMESTAMP
    );
EOFSQL
