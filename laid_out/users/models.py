from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Default custom user model for laid-out.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    # name = CharField(_("Name of User"), blank=True, max_length=36)
    # first_name = None  # type: ignore
    # last_name = None  # type: ignore
