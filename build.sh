#!/usr/bin/env bash

set -o errexit

echo "Running migrations..."
python manage.py migrate --noinput

echo "Resetting admin password..."
python manage.py reset_admin --password="AdminATM@2026"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully."