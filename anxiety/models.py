from datetime import datetime
from django.db import models
from treebeard.mp_tree import MP_Node
from django.core.validators import MaxLengthValidator


class AnxietyTree(MP_Node):
    tree_id = models.CharField(max_length=16)
    date_created = models.DateTimeField("Creation Date", default=datetime.now())
    user = models.CharField(max_length=36, null=True, blank=True)

    title = models.TextField(validators=[MaxLengthValidator(500)])
    description = models.TextField(
        validators=[MaxLengthValidator(5000)], null=True, blank=True
    )

    def __str__(self):
        return f"List: {self.tree_id}Title: {self.title}"

    class Meta:
        verbose_name = "Anxiety Tree"
        verbose_name_plural = "Anxiety Trees"


