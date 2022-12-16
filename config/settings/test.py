"""
With these settings, tests run faster.
"""

from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="bfxUJM1TmBJH5U6SZNGQvc8nsWuqVUlyZxy8Ew43TonbdPd5Re0qqWZeT9qZIMm6",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# DEBUGING FOR TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore # noqa F405

# Other stuff...
# ------------------------------------------------------------------------------
# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": env.str("ENGINE_TEST", default="django.db.backends.postgresql"),
        "NAME": env.str("POSTGRES_DB_TEST", default="pma_database"),
        "USER": env.str("POSTGRES_USER_TEST", default="pma_database"),
        "PASSWORD": env.str("POSTGRES_PASSWORD_TEST", default="pma_database"),
        "HOST": env.str("POSTGRES_HOST_TEST", default="0.0.0.0"),
        "PORT": env.str("POSTGRES_PORT_TEST", default="5433"),
    }
}
