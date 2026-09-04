#!/bin/sh

set -e

echo "Starting Enterprise Business Management System..."

exec uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 2
