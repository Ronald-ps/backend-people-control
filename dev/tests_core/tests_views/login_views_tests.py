import json
import pytest
from http import HTTPStatus
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture()
def user_data(db) -> dict[str, str]:
    data_user = {"username": "username_test", "password": "password_test"}
    User.objects.create_user(**data_user)
    return data_user


# Usar a fixture de client é mais custoso, mas a função "login" do django
# necessita do atributo "session"
def test_login_view(client, user_data):
    response = client.post("/login", data=json.dumps(user_data), content_type="application/json")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["success"] is True


def test_login_view_invalid_user(client, user_data):
    user_data_wrong_user = {"password": user_data["password"], "username": "user_errado"}
    response = client.post("/login", data=json.dumps(user_data_wrong_user), content_type="application/json")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["success"] is False

    user_data_wrong_password = {"password": "senha_errada", "username": user_data["username"]}
    response = client.post(
        "/login", data=json.dumps(user_data_wrong_password), content_type="application/json"
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["success"] is False


def test_login_view_invalid_method(client):
    response = client.get("/login")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_hello_word(client):
    r = client.get("/hello-word")
    assert r.status_code == HTTPStatus.UNAUTHORIZED
