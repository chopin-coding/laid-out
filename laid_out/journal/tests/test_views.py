import pytest
from django.test import Client
from django.urls import reverse

from laid_out.journal.models import Journal
from laid_out.users.models import User

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestJournalPage:
    def test_journal_view_context_authenticated(self, user: User, client: Client):
        client.force_login(user=user)
        response = client.get(reverse("journal:home"))

        assert response.context["logged_in"]
        assert response.context["user_journals"] is not None
        assert response.context["user_journals"][0]["journal_name"] == "New Journal"

    def test_journal_view_context_authenticated_user_with_g_journals(self, user: User, client: Client):
        client.force_login(user=user)
        Journal.objects.create(owner=user, journal_name="custom name")

        response = client.get(reverse("journal:home"))

        assert response.context["logged_in"]
        assert response.context["user_journals"] is not None
        assert response.context["user_journals"][0]["journal_name"] == "custom name"

    def test_journal_view_context_unauthenticated(self, client: Client):
        response = client.get(reverse("journal:home"))

        assert not response.context["logged_in"]
        assert not response.context["user_journals"]

    def test_journal_view_authenticated_user(self, user: User, client: Client):
        # a new user doesn't have any journals
        assert user.journals.all().count() == 0

        client.force_login(user=user)

        response = client.get(reverse("journal:home"))
        assert response is not None

        # the user is automatically assigned a journal after navigating to the journal page
        assert user.journals.all().count() == 1

        response = client.get(reverse("journal:home"))
        assert response is not None
        # the user is not automatically assigned a second journal because they already have one
        assert user.journals.all().count() == 1

    def test_journal_view_anonymous_user(self, client: Client):
        number_of_journals = Journal.objects.all().count()
        response = client.get(reverse("journal:home"))

        assert response is not None
        assert Journal.objects.all().count() == number_of_journals
