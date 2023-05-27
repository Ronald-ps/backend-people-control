import pytest
from model_bakery.baker import make
from rest_framework.test import APIRequestFactory


@pytest.fixture()
def user(db):
    return make("core.User", password="password", username="username", email="user@user.com")


@pytest.fixture
def drf_api_client():
    """Fixture de api cliente para requisição em viewsets"""
    return APIRequestFactory()
