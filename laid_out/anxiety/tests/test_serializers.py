import uuid
from unittest.mock import Mock

import pytest
from rest_framework import serializers

from laid_out.anxiety.models import AnxietyTree, default_tree_data
from laid_out.anxiety.serializers import AnxietyTreeSerializer
from laid_out.users.models import User

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


def test_create_tree_with_valid_data(user: User):
    data = {
        "tree_name": "My Anxiety Tree",
        "tree_data": default_tree_data(),
    }
    request = Mock()
    request.user = user

    serializer = AnxietyTreeSerializer(data=data, context={"request": request})

    assert serializer.is_valid(), serializer.errors
    created_tree = serializer.save()
    assert isinstance(created_tree, AnxietyTree)
    assert created_tree.tree_name == data["tree_name"]
    assert created_tree.tree_data == data["tree_data"]


# TODO: refactor the test
@pytest.mark.skip
def test_create_tree_with_empty_name(user: User):
    data = {
        "tree_name": "",
        "tree_data": default_tree_data(),
    }
    request = Mock()
    request.user = user

    serializer = AnxietyTreeSerializer(data=data, context={"request": request})
    assert serializer.is_valid(), serializer.errors
    created_tree = serializer.save()
    assert created_tree.tree_name == "New Tree"


def test_create_tree_with_too_large_tree_data(user: User):
    # Create a list of strings that exceeds the 50 KB limit
    data = {
        "tree_name": "My Anxiety Tree",
        "tree_data": [{"title": "a" * 52200, "locked": False, "node_id": str(uuid.uuid4()), "children": []}],
    }
    request = Mock()
    request.user = user

    serializer = AnxietyTreeSerializer(data=data, context={"request": request})
    with pytest.raises(serializers.ValidationError) as error:
        serializer.is_valid(raise_exception=True)

    assert "The tree data is too large." in str(error.value.args[0])


def test_create_tree_with_invalid_tree_data(user: User):
    data = {
        "tree_name": "My Anxiety Tree",
        "tree_data": ["invalid data"],
    }
    request = Mock()
    request.user = user

    serializer = AnxietyTreeSerializer(data=data, context={"request": request})

    assert not serializer.is_valid()


def test_update_tree_with_valid_data(user: User):
    existing_tree = AnxietyTree.objects.create(owner=user, tree_name="Original Name", tree_data=default_tree_data())
    updated_data = {
        "tree_name": "Updated Name",
        "tree_data": [{"title": "updated title", "locked": False, "node_id": str(uuid.uuid4()), "children": []}],
    }
    request = Mock()
    request.user = user

    serializer = AnxietyTreeSerializer(instance=existing_tree, data=updated_data, context={"request": request})
    assert serializer.is_valid()
    updated_tree = serializer.save()
    assert updated_tree.pk == existing_tree.pk
    assert updated_tree.tree_name == "Updated Name"
    assert updated_tree.tree_data == updated_data["tree_data"]


def test_update_tree_with_too_large_tree_data(user: User):
    existing_tree = AnxietyTree.objects.create(tree_name="Original Name", tree_data=default_tree_data())
    updated_data = {
        "tree_name": "My Anxiety Tree",
        "tree_data": [{"title": "a" * 52200, "locked": False, "node_id": str(uuid.uuid4()), "children": []}],
    }
    request = Mock()
    request.user = user

    serializer = AnxietyTreeSerializer(instance=existing_tree, data=updated_data)

    with pytest.raises(serializers.ValidationError) as error:
        serializer.is_valid(raise_exception=True)

    assert "The tree data is too large." in str(error.value.args[0])


def test_update_tree_with_invalid_tree_data(user: User):
    existing_tree = AnxietyTree.objects.create(tree_name="Original Name", tree_data=default_tree_data())
    updated_data = {
        "tree_name": "Updated Name",
        "tree_data": ["invalid data"],
    }
    request = Mock()
    request.user = user

    serializer = AnxietyTreeSerializer(instance=existing_tree, data=updated_data, context={"request": request})

    assert not serializer.is_valid()
