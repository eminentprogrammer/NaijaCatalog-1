from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DB_LOCAL_NAME"), #Database Name
        'USER': env("DB_LOCAL_USER"), #Database Username
        'PASSWORD':'@#Demboyz46', #DB Password
        'HOST':'localhost',
        'PORT':'5432',
    }
}
