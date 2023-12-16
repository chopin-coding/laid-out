import pytest
from django.test import Client
from django.urls import reverse

from laid_out.gratitude.models import GratitudeJournal
from laid_out.users.models import User

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestGratitudePage:
    def test_gratitude_view_context_authenticated(self, user: User, client: Client):
        client.force_login(user=user)
        response = client.get(reverse("gratitude:home"))

        assert response.context["logged_in"]
        assert response.context["user_g_journals"] is not None
        assert response.context["user_g_journals"][0]["g_journal_name"] == "New Gratitude"

    def test_gratitude_view_context_authenticated_user_with_g_journals(self, user: User, client: Client):
        client.force_login(user=user)
        GratitudeJournal.objects.create(owner=user, g_journal_name="custom name")

        response = client.get(reverse("gratitude:home"))

        assert response.context["logged_in"]
        assert response.context["user_g_journals"] is not None
        assert response.context["user_g_journals"][0]["g_journal_name"] == "custom name"

    def test_gratitude_view_context_unauthenticated(self, client: Client):
        response = client.get(reverse("gratitude:home"))

        assert not response.context["logged_in"]
        assert not response.context["user_g_journals"]

    def test_gratitude_view_authenticated_user(self, user: User, client: Client):
        # a new user doesn't have any g journals
        assert user.gratitude_journals.all().count() == 0

        client.force_login(user=user)

        response = client.get(reverse("gratitude:home"))
        assert response is not None

        # the user is automatically assigned a g journal after navigating to the gratitude page
        assert user.gratitude_journals.all().count() == 1

        response = client.get(reverse("gratitude:home"))
        assert response is not None
        # the user is not automatically assigned a second g journal because they already have one
        assert user.gratitude_journals.all().count() == 1

    def test_gratitude_view_anonymous_user(self, client: Client):
        number_of_gratitude_journals = GratitudeJournal.objects.all().count()
        response = client.get(reverse("gratitude:home"))

        assert response is not None
        assert GratitudeJournal.objects.all().count() == number_of_gratitude_journals
