import os
from http import HTTPStatus

import dotenv
import pytest
import requests

from reqres_tests.utils.urls import Urls
from reqres_tests.utils.utils import TestData


@pytest.fixture(autouse=True, scope="session")
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL")


@pytest.fixture
def test_data():
    return TestData()


@pytest.fixture
def users():
    response = requests.get(Urls().api_url("users"))
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.fixture
def created_user(test_data):
    user_data = test_data.get_test_user_data()
    response = requests.post(Urls().api_url("users"), json=user_data)
    assert response.status_code == HTTPStatus.CREATED
    return response.json()


@pytest.fixture
def post_delete_user(created_user):
    yield created_user
    response = requests.delete(f"{Urls().api_url('users')}{created_user['id']}", data={})
    assert response.status_code == HTTPStatus.NO_CONTENT
