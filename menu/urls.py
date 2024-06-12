from django.urls import path

from menu.views import UploadMenu

app_name = "menu"

urlpatterns = [
    path("", UploadMenu.as_view(), name="upload_menu")
]
