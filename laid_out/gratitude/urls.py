from django.urls import path

from . import views

app_name = "gratitude"
urlpatterns = [
    path("", views.gratitude_view, name="gratitude-home"),
]
