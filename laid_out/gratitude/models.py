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
