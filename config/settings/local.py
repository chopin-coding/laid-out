import os

from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="biC7mlFM2RUbRnwiVjVGmLPBrIbMn8EBciex6vXDiI6QIqc2O2IaoIZvVgibiWLW",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "192.168.0.70"]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env("EMAIL_HOST", default="mailpit")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa: F405

# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
# INSTALLED_APPS += ["debug_toolbar", "django_browser_reload"]  # noqa: F405

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += [  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # "django_browser_reload.middleware.BrowserReloadMiddleware",
]  # noqa: F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
if env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa: F405
# Celery
# ------------------------------------------------------------------------------

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True
# Your stuff...
# ------------------------------------------------------------------------------
DJANGO_VITE_DEV_MODE = True
CORS_ALLOW_ALL_ORIGINS = True

# Allauth
INSTALLED_APPS += [
    "allauth.socialaccount",
    # "allauth.socialaccount.providers.google",
]  # noqa: F405

allauth_social_loaded = env("ALLAUTH_GOOGLE_AUTH_CLIENT_ID", default=None)

# initialize allauth social login apps only if credentials found;
# this way, anyone can develop locally without allauth social credentials
if allauth_social_loaded:
    INSTALLED_APPS += [
        "allauth.socialaccount.providers.google",
    ]  # noqa: F405

    # SOCIALACCOUNT_ADAPTER = "laid_out.users.adapters.SocialAccountAdapter"
    SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED  # noqa: F405
    SOCIALACCOUNT_EMAIL_REQUIRED = ACCOUNT_EMAIL_REQUIRED  # noqa: F405
    SOCIALACCOUNT_STORE_TOKENS = False

    SOCIALACCOUNT_PROVIDERS = {
        "google": {
            "SCOPE": [
                "email",
            ],
            "AUTH_PARAMS": {
                "access_type": "online",
            },
            "APP": {
                "client_id": env(
                    "ALLAUTH_GOOGLE_AUTH_CLIENT_ID", default=os.environ.get("ALLAUTH_GOOGLE_AUTH_CLIENT_ID")
                ),
                "secret": env("ALLAUTH_GOOGLE_AUTH_SECRET", default=os.environ.get("ALLAUTH_GOOGLE_AUTH_SECRET")),
            },
        }
    }

# TURNSTILE_SITEKEY = None
# TURNSTILE_SECRET = None
