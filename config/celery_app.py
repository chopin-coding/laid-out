import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("laid_out")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "hourly-inactive-user-cleaner": {"task": "laid_out.users.tasks.delete_all_inactive_users_task", "schedule": 3600.0}
}
app.conf.beat_schedule = {
    "daily-db-backup-verifier": {
        "task": "laid_out.users.tasks.verify_db_backup_task",
        # 'schedule': crontab(hour='16', minute='30'),
        "schedule": crontab(),
    },
}
