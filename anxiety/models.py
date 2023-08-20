from django.db import models
from treebeard.mp_tree import MP_Node
from django.core.validators import MaxLengthValidator


class AnxietyList(MP_Node):
    list_id = models.CharField(max_length=16)
    title = models.CharField(max_length=255)
    description = models.TextField(validators=[MaxLengthValidator(5000)], blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
