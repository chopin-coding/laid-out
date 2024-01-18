from datetime import datetime, timedelta, timezone
from logging import getLogger

import boto3
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, EmailMultiAlternatives

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
def delete_all_inactive_users_task() -> None:
    # TODO: make more efficient
    try:
        log.info("Fetching inactive users")
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


@shared_task(rate_limit="1/s")
def send_email_task(email: EmailMultiAlternatives | EmailMessage) -> None:
    try:
        log.info("Starting send_email_task")
        email.send()

    except Exception as e:
        log.error(f"Unexpected error while sending email. email: {email}" f"error: {e}")
        raise


@shared_task(max_retries=3)
def verify_db_backup_task():
    """
    Verifies that the daily backup was uploaded to s3.
    """
    try:
        log.info("Starting verify_db_backup_task")
        s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
        s3_prefix = "backups/"

        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        s3_client = session.client("s3")

        response = s3_client.list_objects_v2(Bucket=s3_bucket, Prefix=s3_prefix)

        if "Contents" in response:
            newest_item = max(obj["LastModified"] for obj in response["Contents"])
            utcnow = datetime.now(timezone.utc)
            time_difference = utcnow - newest_item.astimezone(timezone.utc)

            if time_difference > timedelta(minutes=30):
                log.error("Daily backup not found. Check backup_script.log.")
            else:
                log.info("Daily backup successful.")

        else:
            log.error("No objects found in backups/ folder")
    except Exception as e:
        log.error(f"Unexpected error in verify_db_backup_task: {e}")
        raise
