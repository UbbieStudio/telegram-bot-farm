#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting Telegram Bot Farm Setup for Ubbie..."

# 1. Update the system package list
sudo apt-get update

# 2. Install Docker if it is not already installed
if ! [ -x "$(command -v docker)" ]; then
  echo "📦 Docker not found. Installing now..."
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo usermod -aG docker $USER
  echo "✅ Docker installed successfully."
  rm get-docker.sh
else
  echo "✅ Docker is already installed."
fi

# 3. Create the data directory for Redis persistence
mkdir -p data/redis

# 4. Build and start the containers in detached mode
echo "🏗️ Building and launching your bots..."
docker compose up -d --build

echo "------------------------------------------------"
echo "✅ Farm is up and running!"
echo "To see the logs, run: docker compose logs -f"
echo "To stop the farm, run: docker compose down"
echo "------------------------------------------------"