from django.contrib import admin

from laid_out.goal.models import GoalEntry


@admin.register(GoalEntry)
class GoalEntryAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "data",
        "owner",
        "id",
        "date_modified",
        "date_created",
    ]
    search_fields = ["id"]

    readonly_fields = [
        "id",
        "date_modified",
        "date_created",
    ]
    list_filter = ["date_modified"]
