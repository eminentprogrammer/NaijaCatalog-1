from .base import *


# ALLOWED HOST
RENDER_EXTERNAL_HOSTNAME = env('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DB_NAME"), #Database Name
        'USER': env("DB_USER"), #Database Username
        'PASSWORD':'@#Demboyz46', #DB Password
        'HOST':'localhost',
        'PORT':'5432',
    }
}
