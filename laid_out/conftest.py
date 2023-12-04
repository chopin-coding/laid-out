import pytest
from rest_framework.test import APIClient

from laid_out.users.models import User
from laid_out.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()
