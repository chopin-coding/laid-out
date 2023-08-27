from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from anxiety.models import AnxietyTree, AnxietyTreeMetadata


@admin.register(AnxietyTree)
class AnxietyTreeAdmin(TreeAdmin):
    form = movenodeform_factory(AnxietyTree)

    search_fields = ["metadata_reference__tree_id"]


@admin.register(AnxietyTreeMetadata)
class AnxietyTreeMetadataAdmin(admin.ModelAdmin):
    search_fields = ["tree_id", "user"]
    list_filter = ["date_created"]
