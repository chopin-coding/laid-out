#!/bin/bash

# Determine the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Define the paths to your Docker Compose files
DOCKER_COMPOSE_BACKUP="docker-compose -f $SCRIPT_DIR/production.yml exec -T postgres backup"
DOCKER_COMPOSE_UPLOAD="docker-compose -f $SCRIPT_DIR/production.yml run --rm awscli upload"

# Log file to capture the script output
LOG_FILE="$SCRIPT_DIR/backup_script.log"

# Execute the backup command
echo "$(date): Starting PostgreSQL backup" >> "$LOG_FILE"
$DOCKER_COMPOSE_BACKUP >> "$LOG_FILE" 2>&1

# Execute the upload command
echo "$(date): Starting upload to AWS S3" >> "$LOG_FILE"
$DOCKER_COMPOSE_UPLOAD >> "$LOG_FILE" 2>&1

# Check if the upload was successful (look for the SUCCESS message in the log)
if grep -q "SUCCESS: Finished uploading and cleaning." "$LOG_FILE"; then
    # If successful, delete the backup file
    echo "$(date): Deleting backup file" >> "$LOG_FILE"
    rm -f "${SCRIPT_DIR}/backups/*.sql.gz" >> "$LOG_FILE" 2>&1
fi

echo "$(date): Backup and upload complete" >> "$LOG_FILE"
