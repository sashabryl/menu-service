import pytest
from django.urls import reverse_lazy
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_employee(admin_client: APIClient):
    payload = {
        "username": "employee",
        "password": "asdf!qwe",
        "confirm_password": "asdf!qwe"
    }
    url = reverse_lazy("user:create_employee")
    response = admin_client.post(url, data=payload)

    assert response.status_code == 201
    assert response.data.get("username") == payload.get("username")


@pytest.mark.django_db
def test_create_employee_failure(admin_client: APIClient):
    payload = {
        "username": "employee",
        "password": "asdf!qwe",
        "confirm_password": "asdf!qwe123"
    }
    url = reverse_lazy("user:create_employee")
    response = admin_client.post(url, data=payload)

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_restaurant(admin_client: APIClient):
    payload = {
        "username": "restaurant",
        "password": "asdf!qwe",
        "confirm_password": "asdf!qwe"
    }
    url = reverse_lazy("user:create_restaurant")
    response = admin_client.post(url, data=payload)

    assert response.status_code == 201
    assert response.data.get("username") == payload.get("username")


@pytest.mark.django_db
def test_create_restaurant_failure(admin_client: APIClient):
    payload = {
        "username": "restaurant",
        "password": "asdf!qwe",
        "confirm_password": "asdf!qwe123"
    }
    url = reverse_lazy("user:create_restaurant")
    response = admin_client.post(url, data=payload)

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_restaurant_failure_unique_name(admin_client: APIClient):
    payload = {
        "username": "restaurant",
        "password": "asdf!qwe",
        "confirm_password": "asdf!qwe"
    }
    url = reverse_lazy("user:create_restaurant")
    admin_client.post(url, data=payload)
    response = admin_client.post(url, data=payload)

    assert response.status_code == 400
