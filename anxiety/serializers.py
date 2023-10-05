from pydantic import ValidationError
from rest_framework import serializers
from anxiety.models import AnxietyTree, default_tree_data, TreeData, TreeDataNode

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    anxiety_trees = serializers.PrimaryKeyRelatedField(many=True, queryset=AnxietyTree.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'anxiety_trees']


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
        created = AnxietyTree.objects.create(**validated_data)
        return created

    def update(self, instance, validated_data):
        instance.tree_data = validated_data.get("tree_data")
        instance.tree_name = validated_data.get("tree_name")
        instance.save()

        return instance
