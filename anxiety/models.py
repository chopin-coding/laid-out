import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models


def default_tree_data():
    return {
        "title": "",
        "locked": "false",
        "children": [],
    }


class AnxietyTree(models.Model):
    tree_data_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "locked": {"type": "boolean"},
            "children": {
                "type": "array",
                "items": {"$ref": "#/definitions/node"}
            }
        },
        "definitions": {
            "node": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "locked": {"type": "boolean"},
                    "children": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/node"}
                    }
                }
            }
        }
    }

    tree_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tree_name = models.CharField(
        max_length=30, null=True, blank=True, default="New Tree"
    )
    date_created = models.DateTimeField("Creation Date", auto_now_add=True)
    user = models.CharField(max_length=36, null=True, blank=True)

    tree_data = ArrayField(
        base_field=models.JSONField(default=default_tree_data, null=True, blank=True),
        default=list)

    def __str__(self):
        return f"Name: {self.tree_name} User: {self.user} ID: {self.tree_id}"

    class Meta:
        verbose_name = "Anxiety Tree"
        verbose_name_plural = "Anxiety Trees"
