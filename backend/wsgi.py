import os
import environ
from pathlib import Path
from django.core.wsgi import get_wsgi_application


BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / '.env')
env = environ.Env()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', env("ENV"))
application = get_wsgi_application()
