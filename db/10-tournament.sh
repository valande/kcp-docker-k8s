#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 -d "${POSTGRES_DB}" -U "${POSTGRES_USER}" <<EOFSQL
    CREATE TABLE IF NOT EXISTS tournament (
        player_id SERIAL PRIMARY KEY,
        player VARCHAR (255) NOT NULL,
        points INTEGER NOT NULL DEFAULT 0,
        since date DEFAULT CURRENT_TIMESTAMP
    );
EOFSQL
