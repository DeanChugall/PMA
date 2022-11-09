import os

from django.core.wsgi import get_wsgi_application

from config.settings.base import env

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    env.str("DJANGO_SETTINGS_MODULE", default="config.settings.local"),
)

application = get_wsgi_application()
