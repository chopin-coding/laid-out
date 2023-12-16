from django.contrib import admin

from laid_out.gratitude.models import GratitudeJournal


@admin.register(GratitudeJournal)
class GratitudeJournalAdmin(admin.ModelAdmin):
    fields = [
        "g_journal_name",
        "g_journal_data",
        "owner",
        "g_journal_id",
        "date_modified",
        "date_created",
    ]
    search_fields = ["g_journal_id"]

    readonly_fields = [
        "g_journal_id",
        "date_modified",
        "date_created",
    ]
    list_filter = ["date_modified"]
