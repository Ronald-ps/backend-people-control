import pytest
from http import HTTPStatus
from django.contrib.auth import get_user_model

User = get_user_model()
@pytest.fixture()
def user_data(db) -> dict[str, str]:
    data_user = {
        "username": "username_test",
        "password": "password_test"
    }
    User.objects.create_user(**data_user)
    return data_user

def test_login_view(client, user_data):
    response = client.post("/login", user_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["success"] is True


def test_login_view_invalid_user(client, user_data):
    response = client.post("/login", {"password": "senha_errada", "username": user_data["username"]})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["success"] is False

    response = client.post("/login", {"password": user_data["password"], "username": "user_errado"})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["success"] is False


def test_login_view_invalid_method(client):
    response = client.get("/login")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
