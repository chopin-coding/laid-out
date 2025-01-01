from django.urls import path

from . import views

app_name = "goal"
urlpatterns = [
    path("", views.goal_view, name="home"),
]
