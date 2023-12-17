import uuid

from django.db import models
from pydantic import BaseModel, field_validator

from laid_out import users  # noqa: F401


class JournalData(BaseModel):
    text: str

    @field_validator("text")
    def ensure_text_max_length(cls, v: str) -> str:
        max_length = 100000
        if not len(v) < max_length:
            raise ValueError(f"must be less than {max_length} characters long")
        return v


class Journal(models.Model):
    journal_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    journal_name = models.CharField(max_length=50, null=True, blank=True, default="New Journal")
    date_created = models.DateTimeField(verbose_name="Creation Date", auto_now_add=True)  # UTC
    owner = models.ForeignKey(
        to="users.User",
        related_name="journals",
        # TODO: change on_delete to models.SET_NULL when I implement pagination
        on_delete=models.CASCADE,
        null=True,
    )
    date_modified = models.DateTimeField(auto_now=True)  # UTC

    journal_data = models.TextField(null=True, blank=True, default=str)

    def __str__(self):
        return f"Journal name: {self.journal_name}"

    class Meta:
        verbose_name = "Journal"
        verbose_name_plural = "Journals"
