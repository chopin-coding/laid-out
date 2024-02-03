from unittest.mock import Mock

import pytest
from rest_framework import serializers

from laid_out.journal.models import Journal
from laid_out.journal.serializers import JournalSerializer
from laid_out.users.models import User

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


def test_create_journal_with_valid_data(user: User):
    data = {
        "journal_name": "My Journal",
        "journal_data": "lorem ipsum",
    }
    request = Mock()
    request.user = user

    serializer = JournalSerializer(data=data, context={"request": request})

    assert serializer.is_valid(), serializer.errors
    create_journal = serializer.save()
    assert isinstance(create_journal, Journal)
    assert create_journal.journal_name == data["journal_name"]
    assert create_journal.journal_data == data["journal_data"]


def test_create_journal_with_empty_string(user: User):
    data = {
        "journal_name": "My Journal",
        "journal_data": "",
    }
    request = Mock()
    request.user = user

    serializer = JournalSerializer(data=data, context={"request": request})

    assert serializer.is_valid(), serializer.errors
    create_journal = serializer.save()
    assert isinstance(create_journal, Journal)
    assert create_journal.journal_name == data["journal_name"]
    assert create_journal.journal_data == data["journal_data"]


def test_create_journal_with_empty_name(user: User):
    data = {
        "journal_name": "",
        "journal_data": "",
    }
    request = Mock()
    request.user = user

    serializer = JournalSerializer(data=data, context={"request": request})
    assert serializer.is_valid(), serializer.errors
    create_journal = serializer.save()
    assert create_journal.journal_name == "New Journal"


def test_create_journal_with_too_large_journal_data(user: User):
    max_length = 100000
    data = {
        "journal_name": "My Journal",
        "journal_data": "a" * max_length,
    }
    request = Mock()
    request.user = user

    serializer = JournalSerializer(data=data, context={"request": request})
    with pytest.raises(serializers.ValidationError) as error:
        serializer.is_valid(raise_exception=True)

    assert f"must be less than {max_length} characters long" in str(error.value.args[0])


def test_create_journal_with_invalid_journal_data(user: User):
    data = {
        "journal_name": "My Journal",
        "journal_data": ["invalid data"],
    }
    request = Mock()
    request.user = user

    serializer = JournalSerializer(data=data, context={"request": request})

    assert not serializer.is_valid()


def test_update_journal_with_valid_data(user: User):
    existing_journal = Journal.objects.create(owner=user, journal_name="Original Name", journal_data="")
    updated_data = {
        "journal_name": "Updated Name",
        "journal_data": "lorem ipsum",
    }
    request = Mock()
    request.user = user

    serializer = JournalSerializer(instance=existing_journal, data=updated_data, context={"request": request})
    assert serializer.is_valid()
    updated_journal = serializer.save()
    assert updated_journal.pk == existing_journal.pk
    assert updated_journal.journal_name == "Updated Name"
    assert updated_journal.journal_data == updated_data["journal_data"]


def test_update_journal_with_too_large_journal_data(user: User):
    max_length = 100000
    existing_journal = Journal.objects.create(journal_name="Original Name", journal_data="")
    updated_data = {
        "journal_name": "My Journal",
        "journal_data": "a" * max_length,
    }
    request = Mock()
    request.user = user

    serializer = JournalSerializer(instance=existing_journal, data=updated_data)

    with pytest.raises(serializers.ValidationError) as error:
        serializer.is_valid(raise_exception=True)

    assert f"must be less than {max_length} characters long" in str(error.value.args[0])


def test_update_journal_with_invalid_journal_data(user: User):
    existing_journal = Journal.objects.create(journal_name="Original Name", journal_data="")
    updated_data = {
        "journal_name": "Updated Name",
        "journal_data": [[]],
    }
    request = Mock()
    request.user = user

    serializer = JournalSerializer(instance=existing_journal, data=updated_data, context={"request": request})

    assert not serializer.is_valid()
