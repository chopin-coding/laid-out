from logging import getLogger

from pydantic import ValidationError
from rest_framework import serializers

from laid_out.journal.models import Journal, JournalData

log = getLogger(__name__)


class JournalSerializer(serializers.Serializer):
    journal_id = serializers.UUIDField(read_only=True)
    journal_name = serializers.CharField(max_length=50, required=False, default="New Journal")
    journal_data = serializers.CharField(required=False, default=str, allow_blank=True)
    date_created = serializers.DateTimeField(read_only=True)
    date_modified = serializers.DateTimeField(read_only=True)

    @staticmethod
    def validate_journal_name(data):
        if data == "":
            return "New Journal"
        return data

    @staticmethod
    def validate_journal_data(data):
        # TODO: bleach.py this
        try:
            _ = {"journal_data": JournalData(text=data)}
        except ValidationError as e:
            raise serializers.ValidationError(e)

        return data

    def create(self, validated_data):
        try:
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
            else:
                raise serializers.ValidationError("Journals can only be created by registered users")
            created = Journal.objects.create(owner=user, **validated_data)
            return created
        except Exception as e:
            log.error(f"Unexpected error occurred at JournalSerializer create(): {e}")
            raise

    def update(self, instance, validated_data):
        try:
            instance.journal_data = validated_data.get("journal_data")
            instance.journal_name = validated_data.get("journal_name")
            instance.save()

            return instance
        except Exception as e:
            log.error(f"Unexpected error occurred at JournalSerializer update(): {e}")
            raise
