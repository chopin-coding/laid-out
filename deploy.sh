#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# --- Configuration ---
# Set the application directory and the location of the private deploy key.
APP_DIR="/home/deployer_laid-out/laid-out"
IDENTITY_FILE="/home/deployer_laid-out/.ssh/id_ed25519"

# --- Start Deployment ---
echo "--- Changing to application directory ---"
cd "$APP_DIR" || exit

echo "--- Pulling latest changes from git ---"
# Use an explicit SSH command for Git to ensure the correct key is used,
# especially in minimal environments like CI/CD.
export GIT_SSH_COMMAND="ssh -i $IDENTITY_FILE -o IdentitiesOnly=yes"
git pull
# Unset the variable so it doesn't interfere with other commands.
unset GIT_SSH_COMMAND

echo "--- Sourcing environment for Node/NPM ---"
# Source the Node Version Manager (NVM) script. This is the standard way to
# add node and npm to the PATH in automated scripts.
# This assumes NVM is installed in the deployer_laid-out user's home directory.
if [ -s "$HOME/.nvm/nvm.sh" ]; then
  . "$HOME/.nvm/nvm.sh"
else
  echo "Warning: NVM script not found. NPM commands might fail."
fi

# If your repo has a .nvmrc file, this command will automatically
# switch to the correct Node.js version.
if [ -f ".nvmrc" ]; then
  nvm use
fi

echo "--- Installing/updating NPM dependencies ---"
# Now that the environment is set up, this command should be found.
npm install

echo "--- Restarting application with Docker Compose ---"
# This assumes docker-compose.yml is in the APP_DIR
# Using --build will rebuild images if the Dockerfile has changed.
docker compose up -d --build --remove-orphans

echo "--- Deployment finished successfully ---"
