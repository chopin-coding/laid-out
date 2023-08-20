from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from anxiety.models import AnxietyList


class MyAdmin(TreeAdmin):
    form = movenodeform_factory(AnxietyList)


admin.site.register(AnxietyList, MyAdmin)

