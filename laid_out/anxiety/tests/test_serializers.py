from unittest.mock import Mock

import pytest

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


# def test_create_tree_with_empty_name():
#     data = {
#         "tree_name": "",
#         "tree_data": default_tree_data,
#     }
#     tree = AnxietyTree.objects.create(**data)
#     serializer = AnxietyTreeSerializer(data=tree)
#     assert serializer.is_valid()
#     created_tree = serializer.save()
#     assert created_tree.tree_name == "New Tree"
#
#
# def test_create_tree_with_too_large_tree_data():
#     # Create a list of strings that exceeds the 50 KB limit
#     data = {
#         "tree_name": "My Anxiety Tree",
#         "tree_data": ["x" * 50000] * 10,
#     }
#     serializer = AnxietyTreeSerializer(data=data)
#     with pytest.raises(serializers.ValidationError) as excinfo:
#         serializer.save()
#     assert excinfo.value.args[0] == "The tree data is too large."
#
#
# def test_create_tree_with_invalid_tree_data():
#     data = {
#         "tree_name": "My Anxiety Tree",
#         "tree_data": ["invalid data"],
#     }
#     serializer = AnxietyTreeSerializer(data=data)
#     with pytest.raises(serializers.ValidationError) as excinfo:
#         serializer.save()
#     # Expected error message from pydantic.ValidationError
#     assert excinfo.value.args[0][0]["type"] == "value_error.invalid"
#
#
# def test_update_tree_with_valid_data():
#     existing_tree = AnxietyTree.objects.create(tree_name="Original Name", tree_data=default_tree_data)
#     updated_data = {
#         "tree_name": "Updated Name",
#         "tree_data": ["new data"],
#     }
#     serializer = AnxietyTreeSerializer(instance=existing_tree, data=updated_data)
#     assert serializer.is_valid()
#     updated_tree = serializer.save()
#     assert updated_tree.pk == existing_tree.pk
#     assert updated_tree.tree_name == "Updated Name"
#     assert updated_tree.tree_data == updated_data["tree_data"]
#
#
# def test_update_tree_with_too_large_tree_data():
#     existing_tree = AnxietyTree.objects.create(tree_name="Original Name", tree_data=default_tree_data)
#     updated_data = {
#         "tree_name": "Updated Name",
#         "tree_data": ["x" * 50000] * 10,
#     }
#     serializer = AnxietyTreeSerializer(instance=existing_tree, data=updated_data)
#     with pytest.raises(serializers.ValidationError) as excinfo:
#         serializer.save()
#     assert excinfo.value.args[0] == "The tree data is too large."
#
#
# def test_update_tree_with_invalid_tree_data():
#     existing_tree = AnxietyTree.objects.create(tree_name="Original Name", tree_data=default_tree_data)
#     updated_data = {
#         "tree_name": "Updated Name",
#         "tree_data": ["invalid data"],
#     }
#     serializer = AnxietyTreeSerializer(instance=existing_tree, data=updated_data)
#     with pytest.raises(serializers.ValidationError) as excinfo:
#         serializer.save()
#     # Expected error message from pydantic.ValidationError
#     assert excinfo.value.args[0][0]["type"] == "value_error.invalid"
