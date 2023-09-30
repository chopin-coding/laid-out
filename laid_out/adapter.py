from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError


class UsernameCustomAdapter(DefaultAccountAdapter):
    def clean_username(self, username, **kwargs):
        if not 2 <= len(username) <= 36:
            raise ValidationError('The username should be 2-36 characters long.')
        return DefaultAccountAdapter.clean_username(self, username)  # For other default validations.

