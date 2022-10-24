import os
from config.settings.base import env
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', env.str("DJANGO_SETTINGS_MODULE"))

application = get_wsgi_application()
