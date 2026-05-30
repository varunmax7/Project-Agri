#!/bin/bash
# Backup script for FloodGuard Agri Intelligence database
# This script can be run via cron (e.g., daily at 3 AM)

set -e

BACKUP_DIR="/var/backups/floodguard"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_CONTAINER="floodguard-agri-intelligence-db-1"
DB_USER="floodguard"
DB_NAME="floodguard"

mkdir -p "$BACKUP_DIR"

echo "Starting database backup..."

# Using docker exec to dump from the PostgreSQL container
docker exec $DB_CONTAINER pg_dump -U $DB_USER $DB_NAME | gzip > "$BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz"

echo "Backup created at $BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz"

# Optional: Retain only the last 7 days of backups
find "$BACKUP_DIR" -type f -name "*.sql.gz" -mtime +7 -delete

echo "Old backups cleaned up."
