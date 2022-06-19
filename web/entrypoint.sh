#!/bin/bash
echo "Migrating..."
python3 app.py

echo "Starting..."
exec "$@"