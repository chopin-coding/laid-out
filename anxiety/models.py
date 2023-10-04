import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from pydantic import BaseModel, field_validator, UUID4


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


class AnxietyTree(models.Model):
    tree_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tree_name = models.CharField(
        max_length=50, null=True, blank=True, default="New Tree"
    )
    date_created = models.DateTimeField(verbose_name="Creation Date", auto_now_add=True)
    owner = models.ForeignKey(
        to="auth.User",
        related_name="anxiety_trees",
        on_delete=models.SET_NULL,
        null=True,
    )
    date_modified = models.DateTimeField(auto_now=True)

    tree_data = ArrayField(
        base_field=models.JSONField(null=True, blank=True, default=default_tree_node),
        default=default_tree_data,
    )

    def __str__(self):
        return f"Tree Name: {self.tree_name}"

    class Meta:
        verbose_name = "Anxiety Tree"
        verbose_name_plural = "Anxiety Trees"
