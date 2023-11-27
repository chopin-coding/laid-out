from __future__ import annotations

import typing

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.forms import ValidationError
from django.http import HttpRequest

if typing.TYPE_CHECKING:
    from allauth.socialaccount.models import SocialLogin

    # from laid_out.users.models import User


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    # TODO: perhaps don't allow the username AnonymousUser?
    def clean_username(self, username, **kwargs):
        if not 2 <= len(username) <= 36:
            raise ValidationError("The username should be 2-36 characters long.")
        return DefaultAccountAdapter.clean_username(self, username)  # For other default validations.


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: SocialLogin) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    # def populate_user(self, request: HttpRequest, sociallogin: SocialLogin, data: dict[str, typing.Any]) -> User:
    #     """
    #     Populates user information from social provider info.
    #
    #     See: https://django-allauth.readthedocs.io/en/latest/advanced.html?#creating-and-populating-user-instances
    #     """
    #     user = super().populate_user(request, sociallogin, data)
    #     if not user.name:
    #         if name := data.get("name"):
    #             user.name = name
    #         elif first_name := data.get("first_name"):
    #             user.name = first_name
    #             if last_name := data.get("last_name"):
    #                 user.name += f" {last_name}"
    #     return user

    # TODO: perhaps don't allow the username AnonymousUser?
    def clean_username(self, username, **kwargs):
        if not 2 <= len(username) <= 36:
            raise ValidationError("The username should be 2-36 characters long.")
        return SocialAccountAdapter.clean_username(self, username)  # For other default validations.
