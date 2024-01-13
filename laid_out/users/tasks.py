from logging import getLogger

from celery import shared_task
from django.contrib.auth import get_user_model

log = getLogger(__name__)

User = get_user_model()


@shared_task(max_retries=3)
def delete_user_task(username: str) -> None:
    log.info(f"Starting user deletion for user {username}")
    try:
        user = User.objects.get(username=username)
        user.delete()
        log.info(f"Successfully deleted user {user}")
    except Exception as e:
        log.error(f"Unexpected error while deleting user {username}: {e}")
        raise


@shared_task(max_retries=3)
def delete_all_inactive_users() -> None:
    log.info("Fetching inactive users")
    # TODO: make more efficient
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
                raise
        else:
            log.info("No inactive users found")

    except Exception as e:
        log.error(f"Unexpected error while fetching inactive users: {e}")
        raise
