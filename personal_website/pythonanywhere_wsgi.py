"""
WSGI config for PythonAnywhere deployment.
This is a template. Modify it for your PythonAnywhere username and paths.
"""

import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/Personal_Website/personal_website'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'personal_website.settings'

# Import dotenv and load environment variables
from dotenv import load_dotenv
project_folder = os.path.expanduser('/home/yourusername/Personal_Website/personal_website')
load_dotenv(os.path.join(project_folder, '.env'))

# Set up Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
