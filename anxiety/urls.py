from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"trees", views.AnxietyTreeViewSet, basename="tree")

urlpatterns = [
    path("", views.anxiety_view, name="anxiety_index"),
]

htmx_urlpatterns = [
    path("htmx-test/", views.htmx_test_view, name="htmx-test"),
]

api_urlpatterns = [
    path("api/", include(router.urls)),
    # path("docs/", include_docs_urls(title='Anxiety Tree API')),  # TODO: remove before prod

]

urlpatterns += htmx_urlpatterns
urlpatterns += api_urlpatterns
