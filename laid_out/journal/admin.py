from django.contrib import admin

from laid_out.journal.models import Journal


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    fields = [
        "journal_name",
        "journal_data",
        "owner",
        "journal_id",
        "date_modified",
        "date_created",
    ]
    search_fields = ["journal_id"]

    readonly_fields = [
        "journal_id",
        "date_modified",
        "date_created",
    ]
    list_filter = ["date_modified"]
