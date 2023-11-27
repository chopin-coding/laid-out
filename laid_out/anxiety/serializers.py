from pydantic import ValidationError
from rest_framework import serializers

from laid_out.anxiety.models import AnxietyTree, TreeData, default_tree_data


class AnxietyTreeSerializer(serializers.Serializer):
    tree_id = serializers.UUIDField(read_only=True)
    tree_name = serializers.CharField(max_length=50, required=False)
    tree_data = serializers.ListField(required=False, default=default_tree_data)
    date_created = serializers.DateTimeField(read_only=True)
    date_modified = serializers.DateTimeField(read_only=True)

    @staticmethod
    def validate_tree_name(data):
        if data == "":
            return "New Tree"
        return data

    @staticmethod
    def validate_tree_data(data):
        total_size = 0
        for item in data:
            total_size += len(str(item).encode("utf-8"))
            if total_size > 50 * 1000:  # 50 KB max
                raise serializers.ValidationError("The tree data is too large.")

        try:
            _ = {"tree_data": TreeData(tree_data=data)}
        except ValidationError as e:
            raise serializers.ValidationError(e)

        return data

    def create(self, validated_data):
        try:
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
            else:
                raise serializers.ValidationError("Trees can only be created by registered users")
            created = AnxietyTree.objects.create(owner=user, **validated_data)
            return created
        except Exception as e:
            print(e)

    def update(self, instance, validated_data):
        try:
            instance.tree_data = validated_data.get("tree_data")
            instance.tree_name = validated_data.get("tree_name")
            instance.save()

            return instance
        except Exception as e:
            print(f"Unexpected error when serializing PATCH/PUT: {e}")
