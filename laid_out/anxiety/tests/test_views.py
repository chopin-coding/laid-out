import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import Client, RequestFactory
from django.urls import reverse

from laid_out.anxiety.models import AnxietyTree
from laid_out.anxiety.views import anxiety_view
from laid_out.users.models import User

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestAnxietyPage:
    def test_anxiety_view_context_authenticated(self, user: User, client: Client):
        client.force_login(user=user)
        response = client.get(reverse("anxiety:home"))

        assert response.context["logged_in"]
        assert response.context["user_trees"] is not None
        assert response.context["user_trees"][0]["tree_name"] == "New Tree"

    def test_anxiety_view_context_authenticated_user_with_trees(self, user: User, client: Client):
        client.force_login(user=user)
        AnxietyTree.objects.create(owner=user, tree_name="custom name")

        response = client.get(reverse("anxiety:home"))

        assert response.context["logged_in"]
        assert response.context["user_trees"] is not None
        assert response.context["user_trees"][0]["tree_name"] == "custom name"

    def test_anxiety_view_context_unauthenticated(self, client: Client):
        response = client.get(reverse("anxiety:home"))

        assert not response.context["logged_in"]
        assert not response.context["user_trees"]

    def test_anxiety_view_authenticated_user(self, user: User, rf: RequestFactory):
        rf.user = user

        # a new user doesn't have any anxiety trees
        assert user.anxiety_trees.all().count() == 0

        anxiety_view(request=rf)

        # the user is automatically assigned a tree after navigating to the anxiety page
        assert user.anxiety_trees.all().count() == 1

        anxiety_view(request=rf)

        # the user is not automatically assigned a second tree because they already have one
        assert user.anxiety_trees.all().count() == 1

    def test_anxiety_view_anonymous_user(self, user: User, rf: RequestFactory):
        number_of_anxiety_trees = AnxietyTree.objects.all().count()

        rf.user = AnonymousUser()

        anxiety_view(request=rf)

        # no new anxiety trees are created for after an anonymous user has navigated to the anxiety page
        assert AnxietyTree.objects.all().count() == number_of_anxiety_trees
