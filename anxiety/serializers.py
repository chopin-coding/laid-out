from rest_framework import serializers

from anxiety.models import AnxietyTree


class AnxietyTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnxietyTree
        fields = ["tree_name", 'tree_data', 'date_created', 'user']
