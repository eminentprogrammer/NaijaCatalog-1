import os
import environ
from django.core.wsgi import get_wsgi_application
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR / '.env')

env = environ.Env()  # Load .env file, where env variables are stored


os.environ.setdefault('DJANGO_SETTINGS_MODULE', "backend.settings."+env("ENVIRONMENT"))
application = get_wsgi_application()
