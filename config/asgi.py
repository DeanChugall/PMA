import os

from django.core.asgi import get_asgi_application

from config.settings.base import env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", env.str("DJANGO_SETTINGS_MODULE"))

application = get_asgi_application()
