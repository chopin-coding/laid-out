from logging import getLogger

from celery import shared_task
from django.contrib.auth import get_user_model

from config import celery_app

log = getLogger(__name__)

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@shared_task(max_retries=3)
def delete_user_task(user_name: User) -> None:
    log.info(f"Starting user deletion for user {user_name}")
    try:
        user = User.objects.get(username=user_name)
        user.delete()
        log.info(f"Successfully deleted user {user}")
    except Exception as e:
        log.error(f"Unexpected error while deleting user {user_name}: {e}")


@shared_task(max_retries=3)
def delete_all_inactive_users() -> None:
    log.info("Fetching inactive users")

    try:
        users_to_delete = User.objects.filter(is_active=False)
        if users_to_delete:
            log.info(f"Starting to delete {len(users_to_delete)} inactive users")
            try:
                for user in users_to_delete:
                    user.delete()
                log.info("Successfully deleted all inactive users")
            except Exception as e:
                log.error(f"Unexpected error while deleting inactive users: {e}")
        else:
            log.info("No inactive users found")

    except Exception as e:
        log.error(f"Unexpected error while fetching inactive users: {e}")
