import pytest
from django.urls import reverse_lazy
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_upload_menu(restaurant_client: APIClient):
    payload = {"name": "Menu 1", "description": "The best one"}
    url = reverse_lazy("menu:upload_menu")
    response = restaurant_client.post(url, data=payload)

    assert response.status_code == 201
    assert response.data.get("name") == payload.get("name")


@pytest.mark.django_db
def test_upload_menu_unauthenticated(client: APIClient):
    payload = {"name": "Menu 1", "description": "The best one"}
    url = reverse_lazy("menu:upload_menu")
    response = client.post(url, data=payload)

    assert response.status_code == 401


@pytest.mark.django_db
def test_upload_menu_failure_unique_constraint(restaurant_client: APIClient):
    payload_one = {"name": "Menu 1", "description": "The best one"}
    payload_two = {"name": "Menu 2", "description": "The best two"}
    url = reverse_lazy("menu:upload_menu")
    restaurant_client.post(url, data=payload_one)
    response = restaurant_client.post(url, data=payload_two)

    assert response.status_code == 400


@pytest.mark.django_db
def test_list_menus(employee_client: APIClient, menus):
    url = reverse_lazy("menu:list_menu")
    response = employee_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_list_menus_unauthenticated(client: APIClient, menus):
    url = reverse_lazy("menu:list_menu")
    response = client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_vote_for_menu(employee_client: APIClient, menus):
    first_menu = menus[0]
    url = reverse_lazy("menu:vote_menu", args=[first_menu.id])
    response = employee_client.post(url)
    first_menu.refresh_from_db()

    assert response.status_code == 200
    assert menus[0].num_votes == 1


@pytest.mark.django_db
def test_vote_for_menu_unauthenticated(client: APIClient, menus):
    first_menu = menus[0]
    url = reverse_lazy("menu:vote_menu", args=[first_menu.id])
    response = client.post(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_vote_for_menu_failure_already_voted(
    employee_client: APIClient, menus
):
    first_menu = menus[0]
    url = reverse_lazy("menu:vote_menu", args=[first_menu.id])
    employee_client.post(url)
    response = employee_client.post(url)

    assert response.status_code == 400
