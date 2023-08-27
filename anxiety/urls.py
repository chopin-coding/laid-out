from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("new/", views.anxiety_view, name="anxiety"),
]

htmx_urlpatterns = [path("htmx-test/", views.htmx_test_view, name="htmx-test")]

urlpatterns += htmx_urlpatterns
