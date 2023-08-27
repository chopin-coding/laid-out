from datetime import datetime
from django.db import models
from treebeard.mp_tree import MP_Node
from django.core.validators import MaxLengthValidator


class AnxietyTreeMetadata(models.Model):
    tree_id = models.CharField(max_length=16, unique=True)
    tree_name = models.CharField(
        max_length=30, null=True, blank=True, default="New Tree"
    )
    date_created = models.DateTimeField("Creation Date", default=datetime.now())
    user = models.CharField(max_length=36, null=True, blank=True)

    def __str__(self):
        return f"ID: {self.tree_id} User: {self.user}"

    class Meta:
        verbose_name = "Anxiety Tree Metadata"


class AnxietyTree(MP_Node):
    metadata_reference = models.ForeignKey(AnxietyTreeMetadata, on_delete=models.CASCADE)

    title = models.TextField(validators=[MaxLengthValidator(500)])

    def __str__(self):
        return f"Tree ID: {self.metadata_reference.tree_id} Title: {self.title}"

    class Meta:
        verbose_name = "Anxiety Tree"
        verbose_name_plural = "Anxiety Trees"
