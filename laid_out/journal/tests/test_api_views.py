import pytest
from rest_framework.test import APIClient

from laid_out.journal.models import Journal
from laid_out.users.models import User

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestJournalApiCreateView:
    endpoint = "/api/journals/"

    def test_create_empty_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)

        response = api_client.post(self.endpoint)

        assert response.status_code == 201

    def test_create_valid_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)

        post_data = {
            "journal_name": "test 123",
        }

        response = api_client.post(self.endpoint, data=post_data)

        assert response.status_code == 201

        created_journal = user.journals.get(pk=response.data["journal_id"])

        assert created_journal is not None
        assert created_journal.journal_name == post_data["journal_name"]

    def test_max_number_of_journals(self, user: User, api_client: APIClient):
        for _ in range(151):
            Journal.objects.create(owner=user)
        user_total_journals = user.journals.count()
        api_client.force_login(user=user)

        response = api_client.post(self.endpoint)
        assert response.status_code == 400
        assert user.journals.count() == user_total_journals


class TestJournalApiUpdateView:
    endpoint = "/api/journals/"

    def test_put_valid_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)
        journal_id = api_client.post(self.endpoint).data["journal_id"]

        post_data = {"journal_name": "updated_value"}

        response = api_client.put(self.endpoint + journal_id, data=post_data)
        updated_journal = user.journals.get(pk=journal_id)

        assert response.status_code == 200
        assert updated_journal.journal_name == post_data["journal_name"]

    @pytest.mark.skip  # TODO
    def test_patch_valid_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)
        journal_id = api_client.post(self.endpoint).data["journal_id"]

        post_data = {"journal_name": "updated_value"}

        response = api_client.patch(self.endpoint + journal_id, data=post_data)
        updated_journal = user.journals.get(pk=journal_id)

        assert response.status_code == 200
        assert updated_journal.journal_name == post_data["journal_name"]


class TestJournalApiDeleteView:
    endpoint = "/api/journals/"

    def test_delete(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)
        journal_id = api_client.post(self.endpoint).data["journal_id"]

        response = api_client.delete(self.endpoint + journal_id)

        assert response.status_code == 204

        with pytest.raises(Journal.DoesNotExist):
            user.journals.get(pk=journal_id)

        response = api_client.delete(self.endpoint + journal_id)

        assert response.status_code == 204
