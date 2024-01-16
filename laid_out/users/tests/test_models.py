import pytest

from laid_out.anxiety.models import AnxietyTree
from laid_out.users.models import User

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestUserModel:
    def test_user_anxiety_trees_none(self, user: User):
        assert len(user.anxiety_trees.all()) == 0

    def test_user_anxiety_trees(self, user: User):
        AnxietyTree.objects.create(owner=user)
        assert user.anxiety_trees.count() == 1
