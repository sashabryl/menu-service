from django.urls import path

from menu.views import UploadMenu, ListMenu, vote_for_menu

app_name = "menu"

urlpatterns = [
    path("", ListMenu.as_view(), name="list_menu"),
    path("upload/", UploadMenu.as_view(), name="upload_menu"),
    path("<pk>/vote/", vote_for_menu, name="vote_menu")
]
