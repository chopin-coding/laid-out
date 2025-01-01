import uuid
from unittest.mock import Mock

import pytest
from rest_framework import serializers

from laid_out.goal.models import GoalEntry, default_goal_data
from laid_out.goal.serializers import GoalEntrySerializer
from laid_out.users.models import User

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


def test_create_goal_with_valid_data(user: User):
    data = {
        "name": "My Goal Entry",
        "data": default_goal_data(),
    }
    request = Mock()
    request.user = user

    serializer = GoalEntrySerializer(data=data, context={"request": request})

    assert serializer.is_valid(), serializer.errors
    created_goal = serializer.save()
    assert isinstance(created_goal, GoalEntry)
    assert created_goal.name == data["name"]
    assert created_goal.data == data["data"]


def test_create_goal_with_empty_name(user: User):
    data = {
        "name": "",
        "data": default_goal_data(),
    }
    request = Mock()
    request.user = user

    serializer = GoalEntrySerializer(data=data, context={"request": request})
    assert serializer.is_valid(), serializer.errors
    created_goal = serializer.save()
    assert created_goal.name == "New Goal List"


def test_create_goal_with_too_large_data(user: User):
    # Create a list of strings that exceeds the 50 KB limit
    data = {
        "name": "My Goal Entry",
        "data": [{"title": "a" * 52200, "locked": False, "id": str(uuid.uuid4()), "children": []}],
    }
    request = Mock()
    request.user = user

    serializer = GoalEntrySerializer(data=data, context={"request": request})
    with pytest.raises(serializers.ValidationError) as error:
        serializer.is_valid(raise_exception=True)

    assert "The goal data is too large." in str(error.value.args[0])


def test_create_goal_with_invalid_data(user: User):
    data = {
        "name": "My Goal Entry",
        "data": ["invalid data"],
    }
    request = Mock()
    request.user = user

    serializer = GoalEntrySerializer(data=data, context={"request": request})

    assert not serializer.is_valid()


def test_update_goal_with_valid_data(user: User):
    existing_goal = GoalEntry.objects.create(owner=user, name="Original Name", data=default_goal_data())
    updated_data = {
        "name": "Updated Name",
        "data": [{"title": "updated title", "completed": False, "id": str(uuid.uuid4()), "children": []}],
    }
    request = Mock()
    request.user = user

    serializer = GoalEntrySerializer(instance=existing_goal, data=updated_data, context={"request": request})
    assert serializer.is_valid()
    updated_goal = serializer.save()
    assert updated_goal.pk == existing_goal.pk
    assert updated_goal.name == "Updated Name"
    assert updated_goal.data == updated_data["data"]


def test_update_goal_with_too_large_data(user: User):
    existing_goal = GoalEntry.objects.create(name="Original Name", data=default_goal_data())
    updated_data = {
        "name": "My Goal Entry",
        "data": [{"title": "a" * 52200, "locked": False, "id": str(uuid.uuid4()), "children": []}],
    }
    request = Mock()
    request.user = user

    serializer = GoalEntrySerializer(instance=existing_goal, data=updated_data)

    with pytest.raises(serializers.ValidationError) as error:
        serializer.is_valid(raise_exception=True)

    assert "The goal data is too large." in str(error.value.args[0])


def test_update_goal_with_invalid_data(user: User):
    existing_goal = GoalEntry.objects.create(name="Original Name", data=default_goal_data())
    updated_data = {
        "name": "Updated Name",
        "data": ["invalid data"],
    }
    request = Mock()
    request.user = user

    serializer = GoalEntrySerializer(instance=existing_goal, data=updated_data, context={"request": request})

    assert not serializer.is_valid()
