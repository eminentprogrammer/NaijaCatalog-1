"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import environ
from pathlib import Path
from django.core.asgi import get_asgi_application


BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / '.env')
env = environ.Env()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.ci.production')

application = get_asgi_application()
