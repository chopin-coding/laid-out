import pytest

from laid_out.users.models import User

pytestmark = pytest.mark.django_db


class TestAnxietyApiCreateView:
    endpoint = "/api/trees/"

    def test_authenticated_user(self, user: User):
        pass
