#!/bin/bash

# ManusX Deployment Script
# Usage: ./deploy.sh

set -e

# Configuration
REMOTE_USER="root"
REMOTE_HOST="120.77.218.136"
REMOTE_DIR="/root/manus-x"
LOCAL_PROJECT_DIR="/Users/bytedance/PycharmProjects/manus-x"
PACKAGE_NAME="manus-x.tar.gz"

echo "=========================================="
echo "       ManusX Deployment Script"
echo "=========================================="

# Step 1: Package the project
echo ""
echo "[1/4] Packaging project..."
cd "$(dirname "$LOCAL_PROJECT_DIR")"

tar --exclude='manus-x/.git' \
    --exclude='manus-x/node_modules' \
    --exclude='manus-x/frontend/node_modules' \
    --exclude='manus-x/__pycache__' \
    --exclude='manus-x/**/__pycache__' \
    --exclude='manus-x/**/*.pyc' \
    --exclude='manus-x/.env' \
    -czf "$PACKAGE_NAME" manus-x

PACKAGE_SIZE=$(ls -lh "$PACKAGE_NAME" | awk '{print $5}')
echo "   Package created: $PACKAGE_NAME ($PACKAGE_SIZE)"

# Step 2: Upload to server
echo ""
echo "[2/4] Uploading to server..."
scp "$PACKAGE_NAME" "$REMOTE_USER@$REMOTE_HOST:~/"
echo "   Upload complete"

# Step 3: Deploy on server
echo ""
echo "[3/4] Deploying on server..."
ssh "$REMOTE_USER@$REMOTE_HOST" << 'ENDSSH'
set -e

cd ~

# Backup existing deployment if exists
if [ -d "manus-x" ]; then
    echo "   Backing up existing deployment..."
    rm -rf manus-x.backup
    mv manus-x manus-x.backup
fi

# Extract new package
echo "   Extracting package..."
tar -xzf manus-x.tar.gz

cd manus-x

# Use production config
if [ -f ".env.production" ]; then
    cp .env.production .env
    echo "   Using .env.production"
fi

# Make scripts executable
chmod +x run.sh dev.sh 2>/dev/null || true

# Stop existing containers
echo "   Stopping existing containers..."
docker compose down 2>/dev/null || true

# Start services
echo "   Starting services..."
docker compose up -d

# Wait for services to start
sleep 5

# Show status
echo ""
echo "   Container status:"
docker compose ps

ENDSSH

# Step 4: Clean up local package
echo ""
echo "[4/4] Cleaning up..."
rm -f "$(dirname "$LOCAL_PROJECT_DIR")/$PACKAGE_NAME"
echo "   Done"

echo ""
echo "=========================================="
echo "       Deployment Complete!"
echo "=========================================="
echo ""
echo "Access your application at:"
echo "   http://$REMOTE_HOST:5173"
echo ""
echo "Useful commands (run on server):"
echo "   ./run.sh logs -f      # View logs"
echo "   ./run.sh ps           # Check status"
echo "   ./run.sh down         # Stop services"
echo ""
