import pytest
from rest_framework.test import APIClient

from laid_out.gratitude.models import GratitudeJournal
from laid_out.users.models import User

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestGratitudeJournalApiCreateView:
    endpoint = "/api/gratitude_journals/"

    def test_create_empty_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)

        response = api_client.post(self.endpoint)

        assert response.status_code == 201

    def test_create_valid_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)

        post_data = {
            "g_journal_name": "test 123",
        }

        response = api_client.post(self.endpoint, data=post_data)

        assert response.status_code == 201

        created_g_journal = user.gratitude_journals.get(pk=response.data["g_journal_id"])

        assert created_g_journal is not None
        assert created_g_journal.g_journal_name == post_data["g_journal_name"]

    def test_max_number_of_g_journals(self, user: User, api_client: APIClient):
        for _ in range(151):
            GratitudeJournal.objects.create(owner=user)
        user_total_g_journals = user.gratitude_journals.count()
        api_client.force_login(user=user)

        response = api_client.post(self.endpoint)
        assert response.status_code == 400
        assert user.gratitude_journals.count() == user_total_g_journals


class TestGratitudeJournalApiUpdateView:
    endpoint = "/api/gratitude_journals/"

    def test_put_valid_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)
        g_journal_id = api_client.post(self.endpoint).data["g_journal_id"]

        post_data = {"g_journal_name": "updated_value"}

        response = api_client.put(self.endpoint + g_journal_id, data=post_data)
        updated_g_journal = user.gratitude_journals.get(pk=g_journal_id)

        assert response.status_code == 200
        assert updated_g_journal.g_journal_name == post_data["g_journal_name"]

    @pytest.mark.skip  # TODO
    def test_patch_valid_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)
        g_journal_id = api_client.post(self.endpoint).data["g_journal_id"]

        post_data = {"g_journal_name": "updated_value"}

        response = api_client.patch(self.endpoint + g_journal_id, data=post_data)
        updated_g_journal = user.gratitude_journals.get(pk=g_journal_id)

        assert response.status_code == 200
        assert updated_g_journal.g_journal_name == post_data["g_journal_name"]


class TestGratitudeJournalApiDeleteView:
    endpoint = "/api/gratitude_journals/"

    def test_delete(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)
        g_journal_id = api_client.post(self.endpoint).data["g_journal_id"]

        response = api_client.delete(self.endpoint + g_journal_id)

        assert response.status_code == 204

        with pytest.raises(GratitudeJournal.DoesNotExist):
            user.gratitude_journals.get(pk=g_journal_id)

        response = api_client.delete(self.endpoint + g_journal_id)

        assert response.status_code == 204
