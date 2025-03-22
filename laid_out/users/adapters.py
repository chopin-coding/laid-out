from __future__ import annotations

import typing
from logging import getLogger

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest

from laid_out.users.tasks import send_email_task

log = getLogger(__name__)

if typing.TYPE_CHECKING:
    from allauth.socialaccount.models import SocialLogin

    # from laid_out.users.models import User


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", False)

    def send_mail(self, template_prefix, email, context, *args, **kwargs) -> None:
        try:
            log.info("Starting send_mail")
            ctx = {
                "email": email,
                "current_site": get_current_site(self.request),
            }
            ctx.update(context)
            msg = self.render_mail(template_prefix, email, ctx)

            # adding this here just in case ¯\_(ツ)_/¯
            if len(msg.recipients()) > 1:
                log.error(f"Got multiple recipients for email {email}")
                return

            send_email_task(email=msg)
        except Exception as e:
            log.error(
                "Unexpected error while handing off account email sending to celery. "
                f"template_prefix: {template_prefix}\n"
                f"email: {email}\n"
                f"context: {context}\n"
                f"error: {e}"
            )
            raise


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: SocialLogin) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
