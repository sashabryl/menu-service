from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def admin_client():
    admin = get_user_model().objects.create_superuser(username="admin", password="asdf!qwe")
    client = APIClient()
    client.force_authenticate(admin)
    return client

