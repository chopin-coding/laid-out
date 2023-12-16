import uuid
from unittest.mock import Mock

import pytest
from rest_framework import serializers

from laid_out.gratitude.models import GratitudeJournal, default_g_journal_data
from laid_out.gratitude.serializers import GratitudeJournalSerializer
from laid_out.users.models import User

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


def test_create_g_journal_with_valid_data(user: User):
    data = {
        "g_journal_name": "My Gratitude Journal",
        "g_journal_data": default_g_journal_data(),
    }
    request = Mock()
    request.user = user

    serializer = GratitudeJournalSerializer(data=data, context={"request": request})

    assert serializer.is_valid(), serializer.errors
    create_g_journal = serializer.save()
    assert isinstance(create_g_journal, GratitudeJournal)
    assert create_g_journal.g_journal_name == data["g_journal_name"]
    assert create_g_journal.g_journal_data == data["g_journal_data"]


# TODO: refactor the test
@pytest.mark.skip
def test_create_g_journal_with_empty_name(user: User):
    data = {
        "g_journal_name": "",
        "g_journal_data": default_g_journal_data(),
    }
    request = Mock()
    request.user = user

    serializer = GratitudeJournalSerializer(data=data, context={"request": request})
    assert serializer.is_valid(), serializer.errors
    create_g_journal = serializer.save()
    assert create_g_journal.g_journal_name == "New Gratitude"


def test_create_g_journal_with_too_large_g_journal_data(user: User):
    max_length = 500
    data = {
        "g_journal_name": "My Gratitude",
        "g_journal_data": [{"title": "lorem ipsum", "node_id": str(uuid.uuid4())} for _ in range(max_length)],
    }
    request = Mock()
    request.user = user

    serializer = GratitudeJournalSerializer(data=data, context={"request": request})
    with pytest.raises(serializers.ValidationError) as error:
        serializer.is_valid(raise_exception=True)

    assert f"must be less than {max_length} items long" in str(error.value.args[0])


def test_create_g_journal_with_too_large_g_journal_node(user: User):
    max_length = 10000
    data = {
        "g_journal_name": "My Gratitude",
        "g_journal_data": [{"title": "a" * max_length, "node_id": str(uuid.uuid4())}],
    }
    request = Mock()
    request.user = user

    serializer = GratitudeJournalSerializer(data=data, context={"request": request})
    with pytest.raises(serializers.ValidationError) as error:
        serializer.is_valid(raise_exception=True)

    assert f"must be less than {max_length} characters long" in str(error.value.args[0])


def test_create_g_journal_with_invalid_g_journal_data(user: User):
    data = {
        "g_journal_name": "My Gratitude",
        "g_journal_data": ["invalid data"],
    }
    request = Mock()
    request.user = user

    serializer = GratitudeJournalSerializer(data=data, context={"request": request})

    assert not serializer.is_valid()


def test_update_g_journal_with_valid_data(user: User):
    existing_g_journal = GratitudeJournal.objects.create(
        owner=user, g_journal_name="Original Name", g_journal_data=default_g_journal_data()
    )
    updated_data = {
        "g_journal_name": "Updated Name",
        "g_journal_data": [{"title": "updated title", "locked": False, "node_id": str(uuid.uuid4()), "children": []}],
    }
    request = Mock()
    request.user = user

    serializer = GratitudeJournalSerializer(
        instance=existing_g_journal, data=updated_data, context={"request": request}
    )
    assert serializer.is_valid()
    updated_g_journal = serializer.save()
    assert updated_g_journal.pk == existing_g_journal.pk
    assert updated_g_journal.g_journal_name == "Updated Name"
    assert updated_g_journal.g_journal_data == updated_data["g_journal_data"]


def test_update_g_journal_with_too_large_g_journal_data(user: User):
    max_length = 500
    existing_g_journal = GratitudeJournal.objects.create(
        g_journal_name="Original Name", g_journal_data=default_g_journal_data()
    )
    updated_data = {
        "g_journal_name": "My Gratitude",
        "g_journal_data": [{"title": "lorem ipsum", "node_id": str(uuid.uuid4())} for _ in range(max_length)],
    }
    request = Mock()
    request.user = user

    serializer = GratitudeJournalSerializer(instance=existing_g_journal, data=updated_data)

    with pytest.raises(serializers.ValidationError) as error:
        serializer.is_valid(raise_exception=True)

    assert f"must be less than {max_length} items long" in str(error.value.args[0])


def test_update_g_journal_with_too_large_g_journal_node(user: User):
    max_length = 10000
    existing_g_journal = GratitudeJournal.objects.create(
        g_journal_name="Original Name", g_journal_data=default_g_journal_data()
    )
    updated_data = {
        "g_journal_name": "My Gratitude",
        "g_journal_data": [{"title": "a" * max_length, "node_id": str(uuid.uuid4())}],
    }
    request = Mock()
    request.user = user

    serializer = GratitudeJournalSerializer(instance=existing_g_journal, data=updated_data)

    with pytest.raises(serializers.ValidationError) as error:
        serializer.is_valid(raise_exception=True)

    assert f"must be less than {max_length} characters long" in str(error.value.args[0])


def test_update_g_journal_with_invalid_g_journal_data(user: User):
    existing_g_journal = GratitudeJournal.objects.create(
        g_journal_name="Original Name", g_journal_data=default_g_journal_data()
    )
    updated_data = {
        "g_journal_name": "Updated Name",
        "g_journal_data": [[]],
    }
    request = Mock()
    request.user = user

    serializer = GratitudeJournalSerializer(
        instance=existing_g_journal, data=updated_data, context={"request": request}
    )

    assert not serializer.is_valid()
