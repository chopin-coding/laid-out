import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "laid_out.settings")

app = Celery("laid_out")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
