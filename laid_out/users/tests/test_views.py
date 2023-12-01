import logging

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.messages.storage.fallback import FallbackStorage

from laid_out.users.views import user_delete_view


@pytest.mark.skip
class UserDeleteViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_not_authenticated(self):
        request = self.factory.get(reverse("user_delete"))
        response = user_delete_view(request)
        self.assertRedirects(response, reverse("account_login"))

    def test_delete_user_success(self):
        user = User.objects.create(username="testuser")
        request = self.factory.post(reverse("user_delete"))
        request.user = user

        with self.assertLogs(logging.getLogger(), level="ERROR") as cm:
            response = user_delete_view(request)

        user.refresh_from_db()
        self.assertFalse(user.is_active)
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(
            response.context["messages"].get()[0].message,
            "Your account has been marked for deletion and will be deleted within 24 hours."
        )

    # def test_fetch_user_error(self):
    #     request = self.factory.post(reverse("user_delete"))
    #     request.user = User.objects.create(username="testuser")
    #
    #     with self.assertRaises(ObjectDoesNotExist):
    #         user_delete_view(request)
    #
    #     self.assertRedirects(response, reverse("home"))
    #     self.assertEqual(
    #         response.context["messages"].get()[0].message,
    #         "Unexpected error. Please try again."
    #     )

    def test_delete_account_error(self):
        user = User.objects.create(username="testuser")
        request = self.factory.post(reverse("user_delete"))
        request.user = user

        with self.assertLogs(logging.getLogger(), level="ERROR") as cm:
            response = user_delete_view(request)

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(
            response.context["messages"].get()[0].message,
            "Problem deleting account. Please try again or contact the administrator."
        )
