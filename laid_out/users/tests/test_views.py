import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse

from laid_out.users.models import User
from laid_out.users.views import user_delete_view

pytestmark = pytest.mark.django_db


class TestUserDeleteView:
    def test_user_not_authenticated(self, rf: RequestFactory):
        rf.user = AnonymousUser()

        view = user_delete_view(request=rf)

        # unauthenticated users are redirected to the login page
        assert view.status_code == 302
        assert view.url == reverse("account_login")

    @pytest.mark.skip
    def test_user_authenticated(self, user: User, rf: RequestFactory, settings):
        settings.CELERY_TASK_ALWAYS_EAGER = True
        rf.user = user

        # request = rf.post(reverse("users:delete"))

        assert User.objects.get(username=user.username) is None
