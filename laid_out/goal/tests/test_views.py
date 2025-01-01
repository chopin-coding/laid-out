import pytest
from django.test import Client
from django.urls import reverse

from laid_out.goal.models import GoalEntry
from laid_out.users.models import User

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestGoalPage:
    def test_goal_view_context_authenticated(self, user: User, client: Client):
        client.force_login(user=user)
        response = client.get(reverse("goal:home"))

        assert response.context["logged_in"]

        assert response.context["user_goals"] is not None
        assert response.context["user_goals"][0]["name"] == "Tutorial"

        assert response.context["GOAL_API_BASE_URL"] != ""

    def test_goal_view_context_authenticated_user_with_goals(self, user: User, client: Client):
        client.force_login(user=user)
        GoalEntry.objects.create(owner=user, name="custom name")

        response = client.get(reverse("goal:home"))

        assert response.context["logged_in"]
        assert response.context["user_goals"] is not None
        assert response.context["user_goals"][0]["name"] == "custom name"

    def test_goal_view_context_unauthenticated(self, client: Client):
        response = client.get(reverse("goal:home"))

        assert not response.context["logged_in"]
        assert not response.context["user_goals"]

    def test_goal_view_authenticated_user(self, user: User, client: Client):
        # a new user doesn't have any goal
        assert user.goal_entries.all().count() == 0

        client.force_login(user=user)

        response = client.get(reverse("goal:home"))
        assert response is not None

        # the user is automatically assigned a goal after navigating to the page
        assert user.goal_entries.all().count() == 1

        response = client.get(reverse("goal:home"))
        assert response is not None
        # the user is not automatically assigned a second goal because they already have one
        assert user.goal_entries.all().count() == 1

    def test_goal_view_anonymous_user(self, client: Client):
        number_of_goal_entries = GoalEntry.objects.all().count()
        response = client.get(reverse("goal:home"))

        assert response is not None
        assert GoalEntry.objects.all().count() == number_of_goal_entries
