from django.contrib import admin

from laid_out.anxiety.models import AnxietyTree


@admin.register(AnxietyTree)
class AnxietyTreeAdmin(admin.ModelAdmin):
    fields = [
        "tree_name",
        "tree_data",
        "owner",
        "tree_id",
        "date_modified",
        "date_created",
    ]
    search_fields = ["tree_id"]

    readonly_fields = [
        "tree_id",
        "date_modified",
        "date_created",
    ]
    list_filter = ["date_modified"]
