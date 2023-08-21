from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from anxiety.models import AnxietyList, AnxietyTree


class AnxietyTreeAdmin(TreeAdmin):
    form = movenodeform_factory(AnxietyTree)


class AnxietyListAdmin(admin.ModelAdmin):
    fieldsets = [
        ("List ID", {"fields": ["list_id"]}),
        ("User", {"fields": ["user"]}),
    ]
    list_display = ["list_id", "user"]
    list_filter = ["list_id"]
    search_fields = ["user", "list_id"]


admin.site.register(AnxietyList, AnxietyListAdmin)
admin.site.register(AnxietyTree, AnxietyTreeAdmin)

