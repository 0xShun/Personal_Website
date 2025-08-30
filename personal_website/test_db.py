#!/usr/bin/env python

"""
Test script for PostgreSQL connection.
Run this script to verify database connectivity.
"""

import os
import sys
import django
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_website.settings')
django.setup()

# Now test the database connection
from django.db import connections

def test_db_connection():
    try:
        # Get the default database connection
        connection = connections['default']
        
        # Test the connection
        connection.ensure_connection()
        
        # If we got here, connection was successful
        print("✅ Database connection successful!")
        
        # Get some additional info about the connection
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"Database version: {version}")
        
        # Test a simple query to check permissions
        try:
            cursor.execute("SELECT COUNT(*) FROM django_migrations;")
            count = cursor.fetchone()[0]
            print(f"Found {count} migrations in the database.")
        except Exception as e:
            print(f"Warning: Could not query django_migrations: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        
        # Show database configuration (without sensitive info)
        db_settings = settings.DATABASES['default'].copy()
        if 'PASSWORD' in db_settings:
            db_settings['PASSWORD'] = '******'
        print(f"\nDatabase settings: {db_settings}")
        
        return False

if __name__ == "__main__":
    success = test_db_connection()
    sys.exit(0 if success else 1)
