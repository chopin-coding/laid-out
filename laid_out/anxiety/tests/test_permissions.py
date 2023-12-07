import pytest
from rest_framework.test import APIClient

from laid_out.anxiety.models import AnxietyTree
from laid_out.users.models import User
from laid_out.users.tests.factories import UserFactory

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestAnxietyApiCreatePermissions:
    endpoint = "/api/trees/"

    def test_unauthenticated_user(self, api_client: APIClient):
        response = api_client.post(self.endpoint)

        assert response.status_code == 403
        assert AnxietyTree.objects.count() == 0


# This is just to make sure reading AnxietyTree data in any way is impossible through the API
class TestAnxietyApiGetPermissions:
    endpoint = "/api/trees/"

    def test_get_unavailable_unauthenticated(self, api_client: APIClient):
        tree_id = AnxietyTree.objects.create().pk

        assert api_client.get(self.endpoint).status_code == 403
        assert api_client.get(self.endpoint + str(tree_id)).status_code == 403

    def test_get_unavailable_authenticated(self, user: User, api_client: APIClient):
        tree_id = AnxietyTree.objects.create().pk
        api_client.force_login(user=user)

        assert api_client.get(self.endpoint).status_code == 405
        assert api_client.get(self.endpoint + str(tree_id)).status_code == 405


class TestAnxietyApiUpdatePermissions:
    endpoint = "/api/trees/"

    def test_put_unauthenticated_user(self, user: User, api_client: APIClient):
        authenticated_api_client = APIClient()
        authenticated_api_client.force_login(user=user)
        tree_id = AnxietyTree.objects.create(owner=user).pk

        response = api_client.put(self.endpoint + str(tree_id), data={"tree_name": "update attempt"})

        assert response.status_code == 403

        tree = AnxietyTree.objects.get(pk=tree_id)

        assert tree.tree_name == "New Tree"

    def test_put_authenticated_user(self, user: User, api_client: APIClient):
        tree_id = AnxietyTree.objects.create(owner=user).pk

        second_user = UserFactory()
        api_client.force_login(user=second_user)

        response = api_client.put(self.endpoint + str(tree_id), data={"tree_name": "update attempt"})

        assert response.status_code != 200

        tree = AnxietyTree.objects.get(pk=tree_id)

        assert tree.tree_name == "New Tree"

    def test_patch_unauthenticated_user(self, user: User, api_client: APIClient):
        authenticated_api_client = APIClient()
        authenticated_api_client.force_login(user=user)
        tree_id = AnxietyTree.objects.create(owner=user).pk

        response = api_client.patch(self.endpoint + str(tree_id), data={"tree_name": "update attempt"})

        assert response.status_code == 403

        tree = AnxietyTree.objects.get(pk=tree_id)

        assert tree.tree_name == "New Tree"

    def test_patch_authenticated_user(self, user: User, api_client: APIClient):
        tree_id = AnxietyTree.objects.create(owner=user).pk

        second_user = UserFactory()
        api_client.force_login(user=second_user)

        response = api_client.patch(self.endpoint + str(tree_id), data={"tree_name": "update attempt"})

        assert response.status_code != 200

        tree = AnxietyTree.objects.get(pk=tree_id)

        assert tree.tree_name == "New Tree"


class TestAnxietyApiDeletePermissions:
    endpoint = "/api/trees/"

    def test_unauthenticated_user(self, api_client: APIClient):
        tree_id = AnxietyTree.objects.create().pk

        response = api_client.delete(self.endpoint + str(tree_id))

        assert response.status_code == 403
        assert AnxietyTree.objects.count() == 1

    def test_authenticated_user(self, user: User, api_client: APIClient):
        tree_id = AnxietyTree.objects.create(owner=user).pk

        second_user = UserFactory()
        api_client.force_login(user=second_user)

        response = api_client.delete(self.endpoint + str(tree_id))

        assert response.status_code == 204
        assert user.anxiety_trees.count() == 1
