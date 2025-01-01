import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from pydantic import UUID4, BaseModel, field_validator

from laid_out import users  # noqa: F401


class GoalDataNode(BaseModel):
    title: str
    completed: bool
    children: list["GoalDataNode"]
    id: UUID4

    @field_validator("title")
    def ensure_title_max_length(cls, v: str) -> str:
        max_length = 2000
        if not len(v) < max_length:
            raise ValueError(f"must be less than {max_length} characters long")
        return v


class GoalData(BaseModel):
    data: list[GoalDataNode]


def default_goal_node():
    return {"title": "", "completed": False, "id": str(uuid.uuid4()), "children": []}


def default_goal_data():
    return [default_goal_node()]


def demo_goal_data():
    return [
        {
            "title": "Write down your goals precisely",
            "completed": False,
            "id": "ca6d96c7-0149-4ec0-bf84-e2a65600581e",
            "children": [],
        },
        {
            "title": "Break them",
            "completed": False,
            "id": "b28ddc71-7d7f-4e35-a356-c00b5af839a4",
            "children": [
                {
                    "title": "into parts",
                    "completed": False,
                    "id": "55bb6223-6655-4dfd-80e5-27d1935b3b32",
                    "children": [
                        {
                            "title": "if you'd like",
                            "completed": False,
                            "id": "41344c91-14a4-439a-a471-fded11f73674",
                            "children": [],
                        }
                    ],
                }
            ],
        },
        {
            "title": "Optionally check the ones you completed",
            "completed": True,
            "id": "c0ae7a24-06c9-44de-8eb0-f308a24bb365",
            "children": [],
        },
        {
            "title": "Come back here whenever you lose focus",
            "completed": False,
            "id": "560758f6-aa5a-484a-828c-424f58d40d0a",
            "children": [],
        },
    ]


class GoalEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True, default="New Goal List")
    date_created = models.DateTimeField(verbose_name="Creation Date", auto_now_add=True)  # UTC
    owner = models.ForeignKey(
        to="users.User",
        related_name="goal_entries",
        # TODO: change on_delete to models.SET_NULL when I implement pagination
        on_delete=models.CASCADE,
        null=True,
    )
    date_modified = models.DateTimeField(auto_now=True)  # UTC

    data = ArrayField(
        base_field=models.JSONField(null=True, blank=True, default=default_goal_node),
        default=default_goal_data,
    )

    def __str__(self):
        return f"Goal Name: {self.name}"

    class Meta:
        verbose_name = "Goal Entry"
        verbose_name_plural = "Goal Entries"
