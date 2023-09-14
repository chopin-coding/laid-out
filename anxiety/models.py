import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from pydantic import BaseModel, field_validator


class TreeDataNode(BaseModel):
    title: str
    locked: bool
    children: list['TreeDataNode']

    @field_validator('title')
    def ensure_title_max_length(cls, v: str) -> str:
        max_length = 2000
        if not len(v) < max_length:
            raise ValueError(f'must be less than {max_length} characters long')
        return v


class TreeData(BaseModel):
    tree_data: list[TreeDataNode]


tree_data_json_schema = {
    "$defs": {
        "TreeDataNode": {
            "properties": {
                "title": {
                    "title": "Title",
                    "type": "string"
                },
                "locked": {
                    "title": "Locked",
                    "type": "boolean"
                },
                "children": {
                    "items": {
                        "$ref": "#/$defs/TreeDataNode"
                    },
                    "title": "Children",
                    "type": "array"
                }
            },
            "required": [
                "title",
                "locked",
                "children"
            ],
            "title": "TreeDataNode",
            "type": "object"
        }
    },
    "properties": {
        "tree_data": {
            "items": {
                "$ref": "#/$defs/TreeDataNode"
            },
            "title": "Tree Data",
            "type": "array"
        }
    },
    "required": [
        "tree_data"
    ],
    "title": "TreeData",
    "type": "object"
}


def default_tree_data():
    return [{
        "title": "",
        "locked": False,
        "children": []
    }]


class AnxietyTree(models.Model):
    tree_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tree_name = models.CharField(
        max_length=50, null=True, blank=True, default="New Tree"
    )
    date_created = models.DateTimeField("Creation Date", auto_now_add=True)
    # TODO: an owner is assigned regardless of if the user is authenticated.
    #  gotta prevent people seeing each others shit
    owner = models.ForeignKey('auth.User', related_name='anxiety_trees', on_delete=models.CASCADE, null=True,
                              blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    tree_data = ArrayField(
        base_field=models.JSONField(null=True, blank=True),
        default=list)

    def __str__(self):
        return f"Name: {self.tree_name} Owner: {self.owner}ID: {self.tree_id}"

    class Meta:
        verbose_name = "Anxiety Tree"
        verbose_name_plural = "Anxiety Trees"
