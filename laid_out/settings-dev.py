# this is to run the project locally using dev settings

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
dev_env_file_path = os.path.join(current_dir, "..", "settings.env")

if not load_dotenv(dev_env_file_path):
    raise Exception(f"Couldn't load environment variables in {__file__}.")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = ["*"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# to let urls.py know
os.environ["DEBUG_MODE"] = "True"

INSTALLED_APPS = [
    "django.contrib.admin",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "anxiety",
    "django_vite",
    "debug_toolbar",
    "django_browser_reload",
]

###########
# allauth #
###########

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 15
ACCOUNT_AUTHENTICATION_METHOD = "username_email"

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
# ACCOUNT_SIGNUP_REDIRECT_URL
# ACCOUNT_DEFAULT_HTTP_PROTOCOL
# ACCOUNT_EMAIL_SUBJECT_PREFIX

SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_EMAIL_REQUIRED = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_STORE_TOKENS = False

# ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
# ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400 # 1 day in seconds
LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"

ACCOUNT_ADAPTER = "laid_out.adapter.UsernameCustomAdapter"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
ACCOUNT_EMAIL_VERIFICATION = "optional"  #

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "APP": {
            "client_id": os.environ["ALLAUTH_GOOGLE_AUTH_CLIENT_ID"],
            "secret": os.environ["ALLAUTH_GOOGLE_AUTH_SECRET"],
        },
    }
}

###########
# Logging #
###########

LOG_LEVEL = logging.DEBUG

LOGGING = {
    "version": 1,
    # This will leave the default Django logging behavior in place
    "disable_existing_loggers": False,
    "formatters": {
        "first_formatter": {
            "format": "{asctime} - {levelname} - {module} - {message}",
            "style": "{",
        }
    },
    # Custom handler config that gets log messages and outputs them to console
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,
            "formatter": "first_formatter",
        },
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
    },
    "loggers": {
        # Send everything to console
        "": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
    },
}

#######
# DRF #
#######

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}

# Session lifetime in seconds
#                   <ss> <mm> <hh> <dd>
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7

INTERNAL_IPS = ["127.0.0.1"]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

X_FRAME_OPTIONS = "SAMEORIGIN"

ROOT_URLCONF = "laid_out.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "laid_out.wsgi.application"

##########
# Redis #
##########


##########
# Celery #
##########

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"

############
# Database #
############
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": "db",
        "PORT": 5432,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]

# TODO: Configure these before prod
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/


LANGUAGE_CODE = "en-us"

TIME_ZONE = os.environ.get("TIME_ZONE")

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

###############
# django-vite #
###############

DJANGO_VITE_ASSETS_PATH = BASE_DIR / "static" / "dist"

DJANGO_VITE_DEV_MODE = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / "collectedstatic"
STATIC_URL = "/static/"  # dev
# STATIC_URL = "/static/dist/"  # prod?
STATICFILES_DIRS = [BASE_DIR / "static", DJANGO_VITE_ASSETS_PATH]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
