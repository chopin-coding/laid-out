"""
With these settings, tests run faster.
"""
import os

from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="yF3kGE13F5ZS44CZPLubhFPiHameneodaYNhGuzbP4rVZrP4GlhvETFYGotKCGxU",
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

# DEBUGGING FOR TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore # noqa: F405

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "http://media.testserver"
# Your stuff...
# ------------------------------------------------------------------------------
DJANGO_VITE_DEV_MODE = True

# Allauth

INSTALLED_APPS += [  # noqa: F405
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

# SOCIALACCOUNT_ADAPTER = "laid_out.users.adapters.SocialAccountAdapter"
SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED  # noqa: F405
SOCIALACCOUNT_EMAIL_REQUIRED = ACCOUNT_EMAIL_REQUIRED  # noqa: F405
SOCIALACCOUNT_STORE_TOKENS = False

# https://django-allauth.readthedocs.io/en/latest/forms.html
# ACCOUNT_FORMS = {"signup": "laid_out.users.forms.UserSignupForm"}
# https://django-allauth.readthedocs.io/en/latest/configuration.html
# SOCIALACCOUNT_ADAPTER = "laid_out.users.adapters.SocialAccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/forms.html
# SOCIALACCOUNT_FORMS = {"signup": "laid_out.users.forms.UserSocialSignupForm"}

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "APP": {
            "client_id": env("ALLAUTH_GOOGLE_AUTH_CLIENT_ID", default=os.environ.get("ALLAUTH_GOOGLE_AUTH_CLIENT_ID")),
            "secret": env("ALLAUTH_GOOGLE_AUTH_SECRET", default=os.environ.get("ALLAUTH_GOOGLE_AUTH_SECRET")),
        },
    }
}
