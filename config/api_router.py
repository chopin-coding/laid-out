from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from laid_out.anxiety.views import AnxietyTreeViewSet
from laid_out.goal.views import GoalEntryViewSet
from laid_out.gratitude.views import GratitudeJournalViewSet
from laid_out.journal.views import JournalViewSet


class OptionalSlashDefaultRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = "/?"


class OptionalSlashSimpleRouter(SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = "/?"


if settings.DEBUG:
    router = OptionalSlashDefaultRouter()
    router.register(r"trees", AnxietyTreeViewSet, basename="trees")
    router.register(r"gratitude_journals", GratitudeJournalViewSet, basename="gratitude-journals")
    router.register(r"journals", JournalViewSet, basename="journals")
    router.register(r"goals", GoalEntryViewSet, basename="goals")

else:
    router = OptionalSlashSimpleRouter()
    router.register(r"trees", AnxietyTreeViewSet, basename="trees")
    router.register(r"gratitude_journals", GratitudeJournalViewSet, basename="gratitude-journals")
    router.register(r"journals", JournalViewSet, basename="journals")
    router.register(r"goals", GoalEntryViewSet, basename="goals")

app_name = "api"
urlpatterns = router.urls
