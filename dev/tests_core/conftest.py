import pytest
from model_bakery.baker import make


@pytest.fixture()
def user(db):
    return make("core.User", password="password", username="username", email="user@user.com")
