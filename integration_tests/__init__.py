import os

import django
from django.conf import settings

# Configure django so that our tests work correctly
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'

try:
    # This is how we setup django apps in scripts for django >1.7
    django.setup()
except AttributeError:
    # This is how we do it for older versions of Django
    settings._setup()
