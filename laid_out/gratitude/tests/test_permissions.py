import pytest
from rest_framework.test import APIClient

from laid_out.gratitude.models import GratitudeJournal
from laid_out.users.models import User
from laid_out.users.tests.factories import UserFactory

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestGratitudeJournalApiCreatePermissions:
    endpoint = "/api/gratitude_journals/"

    def test_unauthenticated_user(self, api_client: APIClient):
        response = api_client.post(self.endpoint)

        assert response.status_code == 403
        assert GratitudeJournal.objects.count() == 0


# This is just to make sure reading GratitudeJournal data in any way is impossible through the API
class TestGratitudeJournalApiGetPermissions:
    endpoint = "/api/gratitude_journals/"

    def test_get_unavailable_unauthenticated(self, api_client: APIClient):
        g_journal_id = GratitudeJournal.objects.create().pk

        assert api_client.get(self.endpoint).status_code == 403
        assert api_client.get(self.endpoint + str(g_journal_id)).status_code == 403

    def test_get_unavailable_authenticated(self, user: User, api_client: APIClient):
        g_journal_id = GratitudeJournal.objects.create().pk
        api_client.force_login(user=user)

        assert api_client.get(self.endpoint).status_code == 405
        assert api_client.get(self.endpoint + str(g_journal_id)).status_code == 405


class TestGratitudeJournalApiUpdatePermissions:
    endpoint = "/api/gratitude_journals/"

    def test_put_unauthenticated_user(self, user: User, api_client: APIClient):
        authenticated_api_client = APIClient()
        authenticated_api_client.force_login(user=user)
        g_journal_id = GratitudeJournal.objects.create(owner=user).pk

        response = api_client.put(self.endpoint + str(g_journal_id), data={"g_journal_name": "update attempt"})

        assert response.status_code == 403

        g_journal = GratitudeJournal.objects.get(pk=g_journal_id)

        assert g_journal.g_journal_name == "New Gratitude"

    def test_put_authenticated_user(self, user: User, api_client: APIClient):
        g_journal_id = GratitudeJournal.objects.create(owner=user).pk

        second_user = UserFactory()
        api_client.force_login(user=second_user)

        response = api_client.put(self.endpoint + str(g_journal_id), data={"g_journal_name": "update attempt"})

        assert response.status_code != 200

        g_journal = GratitudeJournal.objects.get(pk=g_journal_id)

        assert g_journal.g_journal_name == "New Gratitude"

    def test_patch_unauthenticated_user(self, user: User, api_client: APIClient):
        authenticated_api_client = APIClient()
        authenticated_api_client.force_login(user=user)
        g_journal_id = GratitudeJournal.objects.create(owner=user).pk

        response = api_client.patch(self.endpoint + str(g_journal_id), data={"g_journal_name": "update attempt"})

        assert response.status_code == 403

        g_journal = GratitudeJournal.objects.get(pk=g_journal_id)

        assert g_journal.g_journal_name == "New Gratitude"

    def test_patch_authenticated_user(self, user: User, api_client: APIClient):
        g_journal_id = GratitudeJournal.objects.create(owner=user).pk

        second_user = UserFactory()
        api_client.force_login(user=second_user)

        response = api_client.patch(self.endpoint + str(g_journal_id), data={"g_journal_name": "update attempt"})

        assert response.status_code != 200

        g_journal = GratitudeJournal.objects.get(pk=g_journal_id)

        assert g_journal.g_journal_name == "New Gratitude"


class TestGratitudeJournalApiDeletePermissions:
    endpoint = "/api/gratitude_journals/"

    def test_unauthenticated_user(self, api_client: APIClient):
        g_journal_id = GratitudeJournal.objects.create().pk

        response = api_client.delete(self.endpoint + str(g_journal_id))

        assert response.status_code == 403
        assert GratitudeJournal.objects.count() == 1

    def test_authenticated_user(self, user: User, api_client: APIClient):
        g_journal_id = GratitudeJournal.objects.create(owner=user).pk

        second_user = UserFactory()
        api_client.force_login(user=second_user)

        response = api_client.delete(self.endpoint + str(g_journal_id))

        assert response.status_code == 204
        assert user.gratitude_journals.count() == 1
