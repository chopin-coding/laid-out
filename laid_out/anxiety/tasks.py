from logging import getLogger

from celery import shared_task
from django.contrib.auth.models import User

log = getLogger(__name__)


@shared_task(max_retries=3)
def delete_user_task(user_name: User):
    log.info(f"Starting user deletion for user {user_name}")
    try:
        user = User.objects.get(username=user_name)
        user.delete()
        log.info(f"Successfully deleted user {user}")
    except Exception as e:
        log.error(f"Unexpected error while deleting user {user_name}: {e}")
