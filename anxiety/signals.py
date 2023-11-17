from logging import getLogger

from allauth.account.models import EmailConfirmation
from allauth.account.signals import user_logged_in, user_logged_out, user_signed_up, password_set, password_changed, \
    password_reset, email_confirmed, email_confirmation_sent, email_changed, email_added, email_removed
from django.contrib import messages
from django.dispatch import receiver

log = getLogger(__name__)


@receiver(user_logged_in)
def user_logged_in_handler(sender, user, **kwargs):
    log.info(f"User {user} logged in.")


@receiver(user_logged_out)
def user_logged_out_handler(sender, user, **kwargs):
    log.info(f"User {user} logged out.")


@receiver(user_signed_up)
def user_signed_up_handler(sender, user, **kwargs):
    log.info(f"User {user} signed up.")


@receiver(password_set)
def password_set_handler(sender, user, **kwargs):
    log.info(f"User {user} set their password.")


@receiver(password_changed)
def password_changed_handler(sender, user, **kwargs):
    log.info(f"User {user} changed their password.")


@receiver(password_reset)
def password_reset_handler(sender, user, **kwargs):
    log.info(f"User {user} reset their password.")


@receiver(email_confirmed)
def email_confirmed_handler(sender, email_address, **kwargs):
    log.info(f"Email address {email_address} confirmed.")


@receiver(email_confirmation_sent)
def email_confirmation_sent_handler(sender, confirmation: EmailConfirmation, signup, **kwargs):
    log.info(f"Email confirmation sent to {confirmation.email_address}. Signup: {signup}")


@receiver(email_changed)
def email_changed_handler(sender, user, from_email_address, to_email_address, **kwargs):
    log.info(f"User {user} changed their email address from {from_email_address} to {to_email_address}.")


@receiver(email_added)
def email_added_handler(sender, user, email_address, **kwargs):
    log.info(f"User {user} added email address {email_address}.")


@receiver(email_removed)
def email_removed_handler(sender, user, email_address, **kwargs):
    log.info(f"User {user} removed email address {email_address}.")
