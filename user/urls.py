from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import CreateEmployee, CreateRestaurant

urlpatterns = [
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("employees/", CreateEmployee.as_view(), name="create_employee"),
    path("restaurants/", CreateRestaurant.as_view(), name="create_restaurant"),
]

app_name = "user"
