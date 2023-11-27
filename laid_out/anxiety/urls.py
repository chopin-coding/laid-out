from django.urls import path

from . import views

app_name = "anxiety"
urlpatterns = [
    path("", views.anxiety_view, name="anxiety-home"),
]
