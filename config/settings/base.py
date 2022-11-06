from pathlib import Path
import environ

# GENERAL
# ------------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / "pma_apps"

env = environ.Env()
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env_dev
    env.read_env(str(ROOT_DIR / ".envs/.local/.django"))
    env.read_env(str(ROOT_DIR / ".envs/.local/.postgres"))
    env.read_env(str(ROOT_DIR / ".envs/.production/.django"))

DEBUG = env.bool("DJANGO_DEBUG", False)

SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="Test")

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "squid-app-ktzit.ondigitalocean.app",
                 "pma-app-k89y6.ondigitalocean.app"]

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_htmx",
]

LOCAL_APPS = [
    'pma_apps.users',
    'pma_apps.auctions',
    'pma_apps.auto_servis',
    'pma_apps.landing_page',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
# Use this for separation if migrations
MIGRATION_MODULES = {
    "auctions": "pma_apps.contrib.auctions.migrations",
    "users": "pma_apps.contrib.users.migrations",
    "auto_servis": "pma_apps.contrib.auto_servis.migrations",
    "landing_page": "pma_apps.contrib.landing_page.migrations",
    "pages": "pma_apps.contrib.landing_page.migrations",
}
# AUTHENTICATION
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = "users.User"

# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [APPS_DIR / 'templates'],
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

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("datatab", "info@dejan.pro")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASES
# ------------------------------------------------------------------------------
# DATABASES = {"default": env.db("DATABASE_URL")}

DATABASES = {
    'default': {
        'ENGINE': env.str("ENGINE", default="django.db.backends.postgresql"),
        'NAME': env.str("POSTGRES_DB", default="pma_database"),
        'USER': env.str("POSTGRES_USER", default="pma_database"),
        'PASSWORD': env.str("POSTGRES_PASSWORD", default="pma_database"),
        'HOST': env.str("POSTGRES_HOST", default="0.0.0.0"),
        'PORT': env.str("POSTGRES_PORT", default="5432"),
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# PASSWORDS
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# INTERNATIONALIZATION
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"


# EMAIL_BACKEND
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", default="")

EMAIL_BACKEND = env.str("EMAIL_BACKEND", default="")
EMAIL_HOST = env.str("EMAIL_HOST", default="")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = env.str("EMAIL_PORT", default="")
EMAIL_USE_TLS = env.str("EMAIL_USE_TLS", default="")
