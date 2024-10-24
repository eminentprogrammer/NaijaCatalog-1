from .base import *

# Unfolding the application
# INSTALLED_APPS += "unfold"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} 
