import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse

from laid_out.users.views import user_delete_view, user_detail_view

pytestmark = pytest.mark.django_db


class TestUserDetailView:
    def test_unauthenticated_user(self, rf: RequestFactory):
        rf.user = AnonymousUser()

        view = user_detail_view(request=rf)

        # unauthenticated users are redirected to the login page
        assert view.status_code == 302
        assert view.url == reverse("account_login")


class TestUserDeleteView:
    def test_user_not_authenticated(self, rf: RequestFactory):
        rf.user = AnonymousUser()

        view = user_delete_view(request=rf)

        # unauthenticated users are redirected to the login page
        assert view.status_code == 302
        assert view.url == reverse("account_login")

    def test_user_authenticated(self):
        # TODO: figure out how to test the view E2E with the celery tasks
        assert True
