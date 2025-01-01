import pytest
from rest_framework.test import APIClient

from laid_out.goal.models import GoalEntry
from laid_out.users.models import User
from laid_out.users.tests.factories import UserFactory

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestGoalApiCreatePermissions:
    endpoint = "/api/goals/"

    def test_unauthenticated_user(self, api_client: APIClient):
        response = api_client.post(self.endpoint)

        assert response.status_code == 403
        assert GoalEntry.objects.count() == 0


# This is just to make sure reading GoalEntry data in any way is impossible through the API
class TestGoalApiGetPermissions:
    endpoint = "/api/goals/"

    def test_get_unavailable_unauthenticated(self, api_client: APIClient):
        id = GoalEntry.objects.create().pk

        assert api_client.get(self.endpoint).status_code == 403
        assert api_client.get(self.endpoint + str(id)).status_code == 403

    def test_get_unavailable_authenticated(self, user: User, api_client: APIClient):
        id = GoalEntry.objects.create().pk
        api_client.force_login(user=user)

        assert api_client.get(self.endpoint).status_code == 405
        assert api_client.get(self.endpoint + str(id)).status_code == 405


class TestGoalApiUpdatePermissions:
    endpoint = "/api/goals/"

    def test_put_unauthenticated_user(self, user: User, api_client: APIClient):
        authenticated_api_client = APIClient()
        authenticated_api_client.force_login(user=user)
        id = GoalEntry.objects.create(owner=user).pk

        response = api_client.put(self.endpoint + str(id), data={"name": "update attempt"})

        assert response.status_code == 403

        goal = GoalEntry.objects.get(pk=id)

        assert goal.name == "New Goal List"

    def test_put_authenticated_user(self, user: User, api_client: APIClient):
        id = GoalEntry.objects.create(owner=user).pk

        second_user = UserFactory()
        api_client.force_login(user=second_user)

        response = api_client.put(self.endpoint + str(id), data={"name": "update attempt"})

        assert response.status_code != 200

        goal = GoalEntry.objects.get(pk=id)

        assert goal.name == "New Goal List"

    def test_patch_unauthenticated_user(self, user: User, api_client: APIClient):
        authenticated_api_client = APIClient()
        authenticated_api_client.force_login(user=user)
        id = GoalEntry.objects.create(owner=user).pk

        response = api_client.patch(self.endpoint + str(id), data={"name": "update attempt"})

        assert response.status_code == 403

        goal = GoalEntry.objects.get(pk=id)

        assert goal.name == "New Goal List"

    def test_patch_authenticated_user(self, user: User, api_client: APIClient):
        id = GoalEntry.objects.create(owner=user).pk

        second_user = UserFactory()
        api_client.force_login(user=second_user)

        response = api_client.patch(self.endpoint + str(id), data={"name": "update attempt"})

        assert response.status_code != 200

        goal = GoalEntry.objects.get(pk=id)

        assert goal.name == "New Goal List"


class TestGoalApiDeletePermissions:
    endpoint = "/api/goals/"

    def test_unauthenticated_user(self, api_client: APIClient):
        id = GoalEntry.objects.create().pk

        response = api_client.delete(self.endpoint + str(id))

        assert response.status_code == 403
        assert GoalEntry.objects.count() == 1

    def test_authenticated_user(self, user: User, api_client: APIClient):
        id = GoalEntry.objects.create(owner=user).pk

        second_user = UserFactory()
        api_client.force_login(user=second_user)

        response = api_client.delete(self.endpoint + str(id))

        assert response.status_code == 204
        assert user.goal_entries.count() == 1
