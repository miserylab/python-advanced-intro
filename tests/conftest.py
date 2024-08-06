import json
import os
from http import HTTPStatus

import dotenv
import pytest
import requests
from faker import Faker

from app_tests.utils.urls import Urls


@pytest.fixture(autouse=True, scope="session")
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL")


@pytest.fixture
def user_test_data():
    faker = Faker("pt_BR")
    return {
        "valid_user_data": {
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "avatar": faker.image_url(),
        },
        "update_user_data": {
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "avatar": faker.image_url(),
        },
        "invalid_email_data": {
            "email": faker.name(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "avatar": faker.image_url(),
        },
        "invalid_avatar_data": {
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "avatar": faker.name(),
        },
    }


@pytest.fixture(scope="session")
def fill_test_data():
    with open("users.json") as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = requests.post(Urls().api_url("users"), json=user)
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        requests.delete(f"{Urls().api_url('users')}{user_id}")


@pytest.fixture
def users(app_url):
    response = requests.get(Urls().api_url("users"))
    assert response.status_code == HTTPStatus.OK
    return response.json()
