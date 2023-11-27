from django.urls import path

from laid_out.users.views import user_delete_view, user_detail_view

app_name = "users"

urlpatterns = [
    path("users/details", view=user_detail_view, name="detail"),
    path("users/delete", view=user_delete_view, name="delete"),
]
