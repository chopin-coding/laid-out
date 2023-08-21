from django.db import models
from treebeard.mp_tree import MP_Node
from django.core.validators import MaxLengthValidator


class AnxietyList(models.Model):
    list_id = models.CharField(max_length=16)
    user = models.CharField(max_length=36)

    def __str__(self):
        return f"List ID: {self.list_id}, User: {self.user}"

    class Meta:
        verbose_name = "Anxiety List"
        verbose_name_plural = "Anxiety Lists"


class AnxietyTree(MP_Node):
    anxiety_list = models.ForeignKey(AnxietyList, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(validators=[MaxLengthValidator(5000)], blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Anxiety Tree"
        verbose_name_plural = "Anxiety Trees"


