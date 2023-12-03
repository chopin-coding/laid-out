import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from laid_out.anxiety.models import AnxietyTree
from laid_out.anxiety.views import anxiety_view
from laid_out.users.models import User

pytestmark = pytest.mark.django_db


class TestAnxietyPage:
    def test_anxiety_view_context_authenticated(self, user: User):
        # TODO
        pass

    def test_anxiety_view_context_unauthenticated(self):
        # TODO
        pass

    def test_anxiety_view_authenticated_user(self, user: User, rf: RequestFactory):
        rf.user = user

        # a new user doesn't have any anxiety trees
        assert len(user.anxiety_trees.all()) == 0

        anxiety_view(request=rf)

        # the user is automatically assigned a tree after navigating to the anxiety page
        assert len(user.anxiety_trees.all()) == 1

        anxiety_view(request=rf)

        # the user is not automatically assigned a second tree because they already have one
        assert len(user.anxiety_trees.all()) == 1

    def test_anxiety_view_anonymous_user(self, user: User, rf: RequestFactory):
        number_of_anxiety_trees = len(AnxietyTree.objects.all())

        rf.user = AnonymousUser()

        anxiety_view(request=rf)

        # no new anxiety trees are created for after an anonymous user has navigated to the anxiety page
        assert len(AnxietyTree.objects.all()) == number_of_anxiety_trees
