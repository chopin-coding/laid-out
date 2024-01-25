import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from pydantic import UUID4, BaseModel, field_validator

from laid_out import users  # noqa: F401


class TreeDataNode(BaseModel):
    title: str
    locked: bool
    children: list["TreeDataNode"]
    node_id: UUID4

    @field_validator("title")
    def ensure_title_max_length(cls, v: str) -> str:
        max_length = 2000
        if not len(v) < max_length:
            raise ValueError(f"must be less than {max_length} characters long")
        return v


class TreeData(BaseModel):
    tree_data: list[TreeDataNode]


def default_tree_node():
    return {"title": "", "locked": False, "node_id": str(uuid.uuid4()), "children": []}


def default_tree_data():
    return [default_tree_node()]


def demo_tree_data():
    return [
        {
            "title": "Welcome to Anxiety!",
            "locked": False,
            "node_id": "7b7308fe-9c1b-4f1a-b081-9463e01ad19c",
            "children": [],
        },
        {
            "title": "Write down your worries",
            "locked": False,
            "node_id": "ca6d96c7-0149-4ec0-bf84-e2a65600581e",
            "children": [],
        },
        {
            "title": "Break each worry down",
            "locked": False,
            "node_id": "b28ddc71-7d7f-4e35-a356-c00b5af839a4",
            "children": [
                {
                    "title": "into parts",
                    "locked": False,
                    "node_id": "55bb6223-6655-4dfd-80e5-27d1935b3b32",
                    "children": [
                        {
                            "title": "if you like",
                            "locked": False,
                            "node_id": "41344c91-14a4-439a-a471-fded11f73674",
                            "children": [],
                        }
                    ],
                }
            ],
        },
        {
            "title": "Cross off the ones that you can't control right now",
            "locked": True,
            "node_id": "a7babe33-46cc-4ff9-88c4-ee16cae90eef",
            "children": [],
        },
        {
            "title": "Accept the ones you can't control right now",
            "locked": False,
            "node_id": "f7fab8b7-4883-4e67-b765-48b1e239e848",
            "children": [],
        },
        {
            "title": "Finally, action the rest",
            "locked": False,
            "node_id": "3d4b4f55-ab54-4aa4-a4be-b476e0e5fc7a",
            "children": [],
        },
        {
            "title": "To get started, create a new anxiety tree!",
            "locked": False,
            "node_id": "19cc5385-aa61-467c-80a6-9f031cd3f715",
            "children": [],
        },
    ]


class AnxietyTree(models.Model):
    tree_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tree_name = models.CharField(max_length=50, null=True, blank=True, default="New Tree")
    date_created = models.DateTimeField(verbose_name="Creation Date", auto_now_add=True)  # UTC
    owner = models.ForeignKey(
        to="users.User",
        related_name="anxiety_trees",
        # TODO: change on_delete to models.SET_NULL when I implement pagination
        on_delete=models.CASCADE,
        null=True,
    )
    date_modified = models.DateTimeField(auto_now=True)  # UTC

    tree_data = ArrayField(
        base_field=models.JSONField(null=True, blank=True, default=default_tree_node),
        default=default_tree_data,
    )

    def __str__(self):
        return f"Tree Name: {self.tree_name}"

    class Meta:
        verbose_name = "Anxiety Tree"
        verbose_name_plural = "Anxiety Trees"
