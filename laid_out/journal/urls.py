from django.urls import path

from . import views

app_name = "journal"
urlpatterns = [
    path("", views.journal_view, name="home"),
]
