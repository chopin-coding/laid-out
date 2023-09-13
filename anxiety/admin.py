from django.contrib import admin

from anxiety.models import AnxietyTree


@admin.register(AnxietyTree)
class AnxietyTreeAdmin(admin.ModelAdmin):

    search_fields = ["tree_id", "user"]

    list_filter = ["date_created"]



