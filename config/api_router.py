from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from laid_out.anxiety.views import AnxietyTreeViewSet


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
else:
    router = OptionalSlashSimpleRouter()
    router.register(r"trees", AnxietyTreeViewSet, basename="trees")

app_name = "api"
urlpatterns = router.urls
