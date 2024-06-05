"""
Database Official Docs
https://docs.djangoproject.com/en/2.1/ref/settings/#databases

"""

from main.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# TODO_CUSTOMIZATION
# Use this if you're using postgres, else change the values accordingly checking the Django docs
DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR + '/prod.sqlite3',
            'USER': None,
            'PASSWORD': None,
            'HOST': None,
            'PORT': None,
        }
}

# TODO_CUSTOMIZATION
DOMAIN_URL = 'http://localhost:8000'
