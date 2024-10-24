from .base import *

DATABASES = {
    'default': dj_database_url.config(
        # Feel free to alter this value to suit your needs.
        default=env("DB_URL"),
        conn_max_age=600
    )
}

# GMAIL CONFIGURATIONS
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587  # For TLS
EMAIL_USE_TLS       = True
EMAIL_USE_SSL       = False  # Set to False for TLS
EMAIL_HOST_USER     = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# ALLOWED HOST
RENDER_EXTERNAL_HOSTNAME = env('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)