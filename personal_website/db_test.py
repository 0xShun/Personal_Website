#!/usr/bin/env python

"""
A simple script to test database connection in a single command.
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_website.settings')

import django
django.setup()

# Test database connection
from django.db import connections

try:
    connection = connections['default']
    connection.ensure_connection()
    print("✅ Database connection successful!")
    print("Connected to:", connection.settings_dict.get('NAME', 'unknown database'))
    
    # Try to execute a simple query
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    print(f"Database version: {version}")
    
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    sys.exit(1)
