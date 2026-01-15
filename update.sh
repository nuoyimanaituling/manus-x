#!/bin/bash

# ManusX Quick Update Script
# Usage: ./update.sh [backend|frontend|all]

set -e

REMOTE_USER="root"
REMOTE_HOST="120.77.218.136"
REMOTE_DIR="/root/manus-x"
LOCAL_DIR="/Users/PycharmProjects/manus-x"

UPDATE_TYPE="${1:-all}"

echo "=========================================="
echo "       ManusX Quick Update"
echo "=========================================="
echo "Update type: $UPDATE_TYPE"
echo ""

# Rsync common options
RSYNC_OPTS="-avz --delete \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.env' \
    --exclude='.env.production' \
    --exclude='*.tar.gz'"

case $UPDATE_TYPE in
    backend)
        echo "[1/2] Syncing backend code..."
        rsync $RSYNC_OPTS "$LOCAL_DIR/backend/" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/backend/"
        rsync $RSYNC_OPTS "$LOCAL_DIR/sandbox/" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/sandbox/"

        echo "[2/2] Restarting backend container..."
        ssh "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_DIR && docker compose restart backend"
        ;;

    frontend)
        echo "[1/2] Syncing frontend code..."
        rsync $RSYNC_OPTS "$LOCAL_DIR/frontend/" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/frontend/"

        echo "[2/2] Rebuilding frontend container..."
        ssh "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_DIR && docker compose up -d --build frontend"
        ;;

    config)
        echo "[1/2] Syncing config files..."
        scp "$LOCAL_DIR/.env.production" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/.env"
        scp "$LOCAL_DIR/docker-compose.yml" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"

        echo "[2/2] Restarting services..."
        ssh "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_DIR && docker compose up -d"
        ;;

    all)
        echo "[1/3] Syncing all code..."
        rsync $RSYNC_OPTS \
            --exclude='frontend/dist' \
            "$LOCAL_DIR/" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"

        echo "[2/3] Syncing production config..."
        scp "$LOCAL_DIR/.env.production" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/.env"

        echo "[3/3] Restarting all services..."
        ssh "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_DIR && docker compose up -d --build"
        ;;

    restart)
        echo "Restarting all services..."
        ssh "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_DIR && docker compose restart"
        ;;

    logs)
        echo "Showing logs (Ctrl+C to exit)..."
        ssh "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_DIR && docker compose logs -f"
        ;;

    status)
        echo "Service status:"
        ssh "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_DIR && docker compose ps"
        ;;

    *)
        echo "Usage: ./update.sh [backend|frontend|config|all|restart|logs|status]"
        echo ""
        echo "Commands:"
        echo "  backend   - Update backend code and restart"
        echo "  frontend  - Update frontend code and rebuild"
        echo "  config    - Update config files and restart"
        echo "  all       - Update everything and rebuild (default)"
        echo "  restart   - Restart all services"
        echo "  logs      - Show live logs"
        echo "  status    - Show container status"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "       Update Complete!"
echo "=========================================="
echo ""
echo "Access: http://$REMOTE_HOST:5173"
echo ""
