import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from pydantic import UUID4, BaseModel, field_validator

from laid_out import users  # noqa: F401


class GratitudeJournalNode(BaseModel):
    title: str
    node_id: UUID4

    @field_validator("title")
    def ensure_title_max_length(cls, v: str) -> str:
        max_length = 10000
        if not len(v) < max_length:
            raise ValueError(f"must be less than {max_length} characters long")
        return v


class GratitudeJournalData(BaseModel):
    data: list[GratitudeJournalNode]

    @field_validator("data")
    def ensure_data_max_length(cls, v: list) -> list:
        max_length = 500
        if not len(v) < max_length:
            raise ValueError(f"must be less than {max_length} items long")
        return v


def default_g_journal_node():
    return {"title": "", "node_id": str(uuid.uuid4())}


def default_g_journal_data():
    return [default_g_journal_node()]


def demo_g_journal_data():
    return [
        {"title": "Write down things you're grateful for", "node_id": "48b1acf5-f2df-4751-9035-af439448d2d4"},
        {
            "title": "It could be a very small thing that happened today",
            "node_id": "152c94c3-7d16-4ea0-bf79-17d3c2a26ca8",
        },
        {"title": "Or something more significant", "node_id": "efc755be-be18-4e7c-9f6c-56adc684c900"},
        {
            "title": "You can write down as many or as few as you'd like",
            "node_id": "f4175def-b4b9-473a-8fc9-7759b5c1f6c4",
        },
        {"title": "5 items a day is great", "node_id": "c881f54a-a947-4963-9cec-9cb95f56a445"},
        {
            "title": 'To get started, create a new gratitude entry via "Create new"',
            "node_id": "7f1704c6-42c3-4ca6-9b45-c4004779c082",
        },
    ]


class GratitudeJournal(models.Model):
    g_journal_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    g_journal_name = models.CharField(max_length=50, null=True, blank=True, default="New Gratitude")
    date_created = models.DateTimeField(verbose_name="Creation Date", auto_now_add=True)  # UTC
    owner = models.ForeignKey(
        to="users.User",
        related_name="gratitude_journals",
        # TODO: change on_delete to models.SET_NULL when I implement pagination
        on_delete=models.CASCADE,
        null=True,
    )
    date_modified = models.DateTimeField(auto_now=True)  # UTC

    g_journal_data = ArrayField(
        base_field=models.JSONField(null=True, blank=True, default=default_g_journal_node),
        default=default_g_journal_data,
    )

    def __str__(self):
        return f"Gratitude journal name: {self.g_journal_name}"

    class Meta:
        verbose_name = "Gratitude Journal"
        verbose_name_plural = "Gratitude Journals"
