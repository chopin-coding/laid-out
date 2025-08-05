#!/bin/bash
set -euo pipefail

# Change to the script's directory to ensure all paths are correct,
# making the script location-independent.
cd "$(dirname "$0")"

echo "--- Pulling latest changes from git ---"
git pull

echo "--- Installing/updating NPM dependencies ---"
npm install

echo "--- Building frontend assets ---"
rm -rf staticfiles
npm run build

echo "--- Stopping and removing old containers, networks, and volumes ---"
# This command is run as the 'deployer_laid-out' user, which, based on your
# systemd service template, should have permissions to manage Docker.
docker compose -f production.yml down --remove-orphans

echo "--- Building fresh Docker images ---"
docker compose -f production.yml build

echo "--- Running database migrations ---"
docker compose -f production.yml run --rm django python manage.py migrate

echo "--- Starting new containers in detached mode ---"
docker compose -f production.yml up -d

echo "--- Removing dangling Docker images ---"
# This safely cleans up unused Docker images without affecting other
# applications running on the same server.
docker image prune -f

echo "--- Deployment finished successfully! ---"
