#!/usr/bin/env bash

set -o errexit

echo "========================================"
echo " ATM SYSTEM - RENDER BUILD"
echo "========================================"

echo "Installing Python dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "========================================"
echo "Running database migrations..."
echo "========================================"

python manage.py migrate --noinput

echo "========================================"
echo "Collecting static files..."
echo "========================================"

python manage.py collectstatic --noinput

echo "========================================"
echo "Creating / updating ATM admin..."
echo "========================================"

python manage.py create_atm_admin || true

echo "========================================"
echo "BUILD COMPLETED SUCCESSFULLY"
echo "========================================"