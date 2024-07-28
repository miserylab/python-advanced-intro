import os
from http import HTTPStatus

import pytest
import requests
from reqres_tests.utils.urls import Urls
from reqres_tests.utils.utils import TestData

import dotenv


@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture
def app_url():
    return os.getenv("APP_URL")


@pytest.fixture
def test_data():
    return TestData()


@pytest.fixture
def users(app_url):
    response = requests.get(f"""{app_url}{Urls().api_url("users")}""")
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.fixture
def created_user(app_url, test_data):
    user_data = test_data.get_test_user_data()
    response = requests.post(f"""{app_url}{Urls().api_url("users")}""", json=user_data)
    assert response.status_code == HTTPStatus.CREATED
    return response.json()


@pytest.fixture
def post_delete_user(app_url, test_data):
    user_data = test_data.get_test_user_data()
    created_user = requests.post(f"""{app_url}{Urls().api_url("users")}""", json=user_data)
    assert created_user.status_code == HTTPStatus.CREATED
    yield created_user.json()
    response = requests.delete(f"""{app_url}{Urls().api_url("users")}{created_user.json()["id"]}""", data={})
    assert response.status_code == HTTPStatus.NO_CONTENT
