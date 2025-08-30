#!/usr/bin/env bash
# exit on error
set -o errexit

# Print versions for debugging
python --version
pip --version

# Install Python dependencies with explicit PostgreSQL support
pip install -r requirements.txt

# Test database connection
python test_db.py || echo "Database connection test failed, but continuing build..."

# Run Django commands
python manage.py collectstatic --noinput
python manage.py migrate

echo "Build completed successfully!"
