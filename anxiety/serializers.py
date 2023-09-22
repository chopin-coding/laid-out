import jsonschema
from rest_framework import serializers
from anxiety.models import AnxietyTree, tree_data_json_schema, default_tree_data


class AnxietyTreeSerializer(serializers.Serializer):
    tree_id = serializers.UUIDField(read_only=True)
    tree_name = serializers.CharField(max_length=50, required=False)
    tree_data = serializers.ListField(required=False, default=default_tree_data)

    def validate_tree_name(self, data):
        if data == "":
            return "New Tree"
        return data

    def validate_tree_data(self, data):
        total_size = 0
        for item in data:
            total_size += len(str(item).encode("utf-8"))
            if total_size > 50 * 1000:  # 50 KB max
                raise serializers.ValidationError("The tree data is too large.")

        try:
            jsonschema.validate(
                instance={"tree_data": data}, schema=tree_data_json_schema
            )
        except jsonschema.exceptions.ValidationError as e:
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