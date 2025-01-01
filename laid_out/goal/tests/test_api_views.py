import pytest
from rest_framework.test import APIClient

from laid_out.goal.models import GoalEntry
from laid_out.users.models import User

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestGoalApiCreateView:
    endpoint = "/api/goals/"

    def test_create_empty_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)

        response = api_client.post(self.endpoint)

        assert response.status_code == 201

    def test_create_valid_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)

        post_data = {
            "name": "test 123",
        }

        response = api_client.post(self.endpoint, data=post_data)

        assert response.status_code == 201

        created_goal = user.goal_entries.get(pk=response.data["id"])

        assert created_goal is not None
        assert created_goal.name == post_data["name"]

    def test_max_number_of_goal_entries(self, user: User, api_client: APIClient):
        for _ in range(151):
            GoalEntry.objects.create(owner=user)
        user_total_goals = user.goal_entries.count()
        api_client.force_login(user=user)

        response = api_client.post(self.endpoint)
        assert response.status_code == 400
        assert user.goal_entries.count() == user_total_goals


class TestGoalsApiUpdateView:
    endpoint = "/api/goals/"

    def test_put_valid_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)
        id = api_client.post(self.endpoint).data["id"]

        post_data = {"name": "updated_value"}

        response = api_client.put(self.endpoint + id, data=post_data)
        updated_goal = user.goal_entries.get(pk=id)

        assert response.status_code == 200
        assert updated_goal.name == post_data["name"]

    @pytest.mark.skip  # TODO
    def test_patch_valid_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)
        id = api_client.post(self.endpoint).data["id"]

        post_data = {"name": "updated_value"}

        response = api_client.patch(self.endpoint + id, data=post_data)
        updated_goal = user.goal_entries.get(pk=id)

        assert response.status_code == 200
        assert updated_goal.name == post_data["name"]


class TestGoalsApiDeleteView:
    endpoint = "/api/goals/"

    def test_delete(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)
        id = api_client.post(self.endpoint).data["id"]

        response = api_client.delete(self.endpoint + id)

        assert response.status_code == 204

        with pytest.raises(GoalEntry.DoesNotExist):
            user.goal_entries.get(pk=id)

        response = api_client.delete(self.endpoint + id)

        assert response.status_code == 204
