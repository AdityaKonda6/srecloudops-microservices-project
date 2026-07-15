#!/bin/bash
set -e

# Create multiple databases (split by comma)
IFS=',' read -ra DATABASES <<< "$POSTGRES_MULTIPLE_DATABASES"
for db in "${DATABASES[@]}"; do
  # Trim whitespace
  db=$(echo "$db" | xargs)
  echo "Creating database $db..."
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE $db;
EOSQL
done

echo "Database initialization complete"
