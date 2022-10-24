import os
from config.settings.base import env
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', env.str("DJANGO_SETTINGS_MODULE"))

application = get_asgi_application()
