from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest

from menu.models import Menu


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def admin_client():
    admin = get_user_model().objects.create_superuser(
        username="admin", password="asdf!qwe"
    )
    client = APIClient()
    client.force_authenticate(admin)
    return client


@pytest.fixture
def restaurant_client():
    restaurant = get_user_model().objects.create_user(
        username="restaurant",
        password="asdf!qwe",
        is_restaurant=True
    )
    client= APIClient()
    client.force_authenticate(restaurant)
    return client


@pytest.fixture
def employee_client():
    employee = get_user_model().objects.create_user(
        username="employee",
        password="asdf!qwe",
        is_employee=True
    )
    client= APIClient()
    client.force_authenticate(employee)
    return client


@pytest.fixture
def menus():
    restaurant1 = get_user_model().objects.create_user(
        username="restaurant1",
        password="asdf!qwe",
        is_restaurant=True
    )
    restaurant2 = get_user_model().objects.create_user(
        username="restaurant2",
        password="asdf!qwe",
        is_restaurant=True
    )
    menu_1 = Menu.objects.create(
        name="Menu 1", description="Marvelous", restaurant=restaurant1
    )
    menu_2 = Menu.objects.create(
        name="Menu 2", description="Marvelous", restaurant=restaurant2
    )
    return [menu_1, menu_2]
