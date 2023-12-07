import pytest
from rest_framework.test import APIClient

from laid_out.anxiety.models import AnxietyTree
from laid_out.users.models import User

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestAnxietyApiCreateView:
    endpoint = "/api/trees/"

    def test_create_empty_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)

        response = api_client.post(self.endpoint)

        assert response.status_code == 201

    def test_create_valid_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)

        post_data = {
            "tree_name": "test 123",
        }

        response = api_client.post(self.endpoint, data=post_data)

        assert response.status_code == 201

        created_tree = user.anxiety_trees.get(pk=response.data["tree_id"])

        assert created_tree is not None
        assert created_tree.tree_name == post_data["tree_name"]


class TestAnxietyApiUpdateView:
    endpoint = "/api/trees/"

    def test_put_valid_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)
        tree_id = api_client.post(self.endpoint).data["tree_id"]

        post_data = {"tree_name": "updated_value"}

        response = api_client.put(self.endpoint + tree_id, data=post_data)
        updated_tree = user.anxiety_trees.get(pk=tree_id)

        assert response.status_code == 200
        assert updated_tree.tree_name == post_data["tree_name"]

    @pytest.mark.skip  # FIXME
    def test_patch_valid_data(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)
        tree_id = api_client.post(self.endpoint).data["tree_id"]

        post_data = {"tree_name": "updated_value"}

        response = api_client.patch(self.endpoint + tree_id, data=post_data)
        updated_tree = user.anxiety_trees.get(pk=tree_id)

        assert response.status_code == 200
        assert updated_tree.tree_name == post_data["tree_name"]


class TestAnxietyApiDeleteView:
    endpoint = "/api/trees/"

    def test_delete(self, user: User, api_client: APIClient):
        api_client.force_login(user=user)
        tree_id = api_client.post(self.endpoint).data["tree_id"]

        response = api_client.delete(self.endpoint + tree_id)

        assert response.status_code == 204

        with pytest.raises(AnxietyTree.DoesNotExist):
            user.anxiety_trees.get(pk=tree_id)

        response = api_client.delete(self.endpoint + tree_id)

        assert response.status_code == 204
