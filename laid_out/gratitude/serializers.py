from logging import getLogger

from pydantic import ValidationError
from rest_framework import serializers

from laid_out.gratitude.models import GratitudeJournal, GratitudeJournalData, default_g_journal_data

log = getLogger(__name__)


class GratitudeJournalSerializer(serializers.Serializer):
    g_journal_id = serializers.UUIDField(read_only=True)
    g_journal_name = serializers.CharField(max_length=255, allow_blank=True, required=False, default="New Gratitude")
    g_journal_data = serializers.ListField(required=False, default=default_g_journal_data)
    date_created = serializers.DateTimeField(read_only=True)
    date_modified = serializers.DateTimeField(read_only=True)

    @staticmethod
    def validate_g_journal_name(data):
        if data == "":
            return "New Gratitude"
        return data

    @staticmethod
    def validate_g_journal_data(data):
        try:
            _ = {"g_journal_data": GratitudeJournalData(data=data)}
        except ValidationError as e:
            raise serializers.ValidationError(e)

        return data

    def create(self, validated_data):
        try:
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
            else:
                raise serializers.ValidationError("Gratitude journals can only be created by registered users")
            created = GratitudeJournal.objects.create(owner=user, **validated_data)
            return created
        except Exception as e:
            log.error(f"Unexpected error occurred at GratitudeJournalSerializer create(): {e}")
            raise

    def update(self, instance, validated_data):
        try:
            instance.g_journal_data = validated_data.get("g_journal_data")
            instance.g_journal_name = validated_data.get("g_journal_name")
            instance.save()

            return instance
        except Exception as e:
            log.error(f"Unexpected error occurred at GratitudeJournalSerializer update(): {e}")
            raise
