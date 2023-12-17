import pytest
from rest_framework.test import APIClient

from laid_out.journal.models import Journal
from laid_out.users.models import User
from laid_out.users.tests.factories import UserFactory

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestJournalApiCreatePermissions:
    endpoint = "/api/journals/"

    def test_unauthenticated_user(self, api_client: APIClient):
        response = api_client.post(self.endpoint)

        assert response.status_code == 403
        assert Journal.objects.count() == 0


# This is just to make sure reading Journal data in any way is impossible through the API
class TestJournalApiGetPermissions:
    endpoint = "/api/journals/"

    def test_get_unavailable_unauthenticated(self, api_client: APIClient):
        journal_id = Journal.objects.create().pk

        assert api_client.get(self.endpoint).status_code == 403
        assert api_client.get(self.endpoint + str(journal_id)).status_code == 403

    def test_get_unavailable_authenticated(self, user: User, api_client: APIClient):
        journal_id = Journal.objects.create().pk
        api_client.force_login(user=user)

        assert api_client.get(self.endpoint).status_code == 405
        assert api_client.get(self.endpoint + str(journal_id)).status_code == 405


class TestJournalApiUpdatePermissions:
    endpoint = "/api/journals/"

    def test_put_unauthenticated_user(self, user: User, api_client: APIClient):
        authenticated_api_client = APIClient()
        authenticated_api_client.force_login(user=user)
        journal_id = Journal.objects.create(owner=user).pk

        response = api_client.put(self.endpoint + str(journal_id), data={"journal_name": "update attempt"})

        assert response.status_code == 403

        journal = Journal.objects.get(pk=journal_id)

        assert journal.journal_name == "New Journal"

    def test_put_authenticated_user(self, user: User, api_client: APIClient):
        journal_id = Journal.objects.create(owner=user).pk

        second_user = UserFactory()
        api_client.force_login(user=second_user)

        response = api_client.put(self.endpoint + str(journal_id), data={"journal_name": "update attempt"})

        assert response.status_code != 200

        journal = Journal.objects.get(pk=journal_id)

        assert journal.journal_name == "New Journal"

    def test_patch_unauthenticated_user(self, user: User, api_client: APIClient):
        authenticated_api_client = APIClient()
        authenticated_api_client.force_login(user=user)
        journal_id = Journal.objects.create(owner=user).pk

        response = api_client.patch(self.endpoint + str(journal_id), data={"journal_name": "update attempt"})

        assert response.status_code == 403

        journal = Journal.objects.get(pk=journal_id)

        assert journal.journal_name == "New Journal"

    def test_patch_authenticated_user(self, user: User, api_client: APIClient):
        journal_id = Journal.objects.create(owner=user).pk

        second_user = UserFactory()
        api_client.force_login(user=second_user)

        response = api_client.patch(self.endpoint + str(journal_id), data={"journal_name": "update attempt"})

        assert response.status_code != 200

        journal = Journal.objects.get(pk=journal_id)

        assert journal.journal_name == "New Journal"


class TestJournalApiDeletePermissions:
    endpoint = "/api/journals/"

    def test_unauthenticated_user(self, api_client: APIClient):
        journal_id = Journal.objects.create().pk

        response = api_client.delete(self.endpoint + str(journal_id))

        assert response.status_code == 403
        assert Journal.objects.count() == 1

    def test_authenticated_user(self, user: User, api_client: APIClient):
        journal_id = Journal.objects.create(owner=user).pk

        second_user = UserFactory()
        api_client.force_login(user=second_user)

        response = api_client.delete(self.endpoint + str(journal_id))

        assert response.status_code == 204
        assert user.journals.count() == 1
