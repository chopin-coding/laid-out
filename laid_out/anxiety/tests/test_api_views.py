import pytest
from rest_framework.test import APIClient

from laid_out.users.models import User

pytestmark = pytest.mark.django_db


class TestAnxietyApiCreateView:
    endpoint = "/api/trees/"

    def test_create(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)

        response = api_client.post(self.endpoint)

        assert response.status_code == 201
