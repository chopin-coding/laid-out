from logging import getLogger

from pydantic import ValidationError
from rest_framework import serializers

from laid_out.goal.models import GoalData, GoalEntry, default_goal_data

log = getLogger(__name__)


class GoalEntrySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=255, allow_blank=True, required=False, default="New Goal List")
    data = serializers.ListField(required=False, default=default_goal_data)
    date_created = serializers.DateTimeField(read_only=True)
    date_modified = serializers.DateTimeField(read_only=True)

    @staticmethod
    def validate_name(data):
        if data == "":
            return "New Goal List"
        return data

    @staticmethod
    def validate_data(data):
        total_size = 0
        for item in data:
            total_size += len(str(item).encode("utf-8"))
            if total_size > 50 * 1000:  # 50 KB max
                raise serializers.ValidationError("The goal data is too large.")

        try:
            _ = {"data": GoalData(data=data)}
        except ValidationError as e:
            raise serializers.ValidationError(e)

        return data

    def create(self, validated_data):
        try:
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
            else:
                raise serializers.ValidationError("Goal entries can only be created by registered users")
            created = GoalEntry.objects.create(owner=user, **validated_data)
            return created
        except Exception as e:
            log.error(f"Unexpected error occurred at GoalEntrySerializer create(): {e}")
            raise

    def update(self, instance, validated_data):
        try:
            instance.data = validated_data.get("data")
            instance.name = validated_data.get("name")
            instance.save()

            return instance
        except Exception as e:
            log.error(f"Unexpected error occurred at GoalEntrySerializer update(): {e}")
            raise
