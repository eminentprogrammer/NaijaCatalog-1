import os
import environ
import cloudinary
import dj_database_url
# from .jazzmin import *
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR / '.env')

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

DEBUG           = True

SECRET_KEY      = env("SECRET_KEY")

ALLOWED_HOSTS   = ["*"]

# Application definition
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.import_export",
    "unfold.contrib.forms",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    
    'whitenoise',
    "crispy_forms",
    "crispy_bootstrap5",
    'django.contrib.staticfiles',
    'import_export',

    'frontend',
    'https',
    'blog',
    'apps.accounts',
    'apps.catalogue',
    'apps.emailApp',
    'apps.partners',

    # HEALTH CHECK SETTINGS
    'health_check',
    'health_check.contrib.psutil',
    'health_check.db',  
    # stock Django health checkers
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.migrations',
]

HEALTH_CHECK = {
    'DISK_USAGE_MAX': 90, #Percent
    'MEMORY_MIN': 100, # in MB
}


HEALTH_CHECK['DISK_USAGE_MAX'] = 5 * (1 << 30)   # 5GB in bytes

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_USER_MODEL  = 'accounts.Account'
WSGI_APPLICATION = 'backend.wsgi.application'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    } 
else: 
    DATABASES = {
        'default': dj_database_url.config(
            # Feel free to alter this value to suit your needs.
            default=env("DB_URL"),
            conn_max_age=600
        )
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = 'static/'
MEDIA_URL = 'media/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'plugins/static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'plugins/assets')
MEDIA_ROOT = os.path.join(BASE_DIR, 'plugins/media')

# Following settings only make sense on production and may break development environments.
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CLOUDINARY SETTINGS FOR IMAGE STORAGE
cloudinary.config(
    cloud_name = env("CLOUDINARY_NAME"),
    api_key    = env("CLOUDINARY_API_KEY"),
    api_secret = env("CLOUDINARY_API_SECRET"),
)

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


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

UNFOLD = {
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
                "nl": "🇧🇪",
            },
        },
    },
}