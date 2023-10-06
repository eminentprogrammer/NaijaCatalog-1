from .base import *

# ALLOWED HOST
RENDER_EXTERNAL_HOSTNAME = env('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

DATABASES = {
    'default': dj_database_url.config(
        # Feel free to alter this value to suit your needs.
        default=env("DB_URL"),
        conn_max_age=600
    )
}