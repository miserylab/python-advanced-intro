from http import HTTPStatus

import pytest
import requests

from reqres_app.models.user_model import User
from reqres_tests.utils.urls import Urls


class TestApi:
    def test_users(self, app_url):
        response = requests.get(f"""{app_url}{Urls().api_url("users")}""")
        assert response.status_code == HTTPStatus.OK

        user_list = response.json()["items"]
        for user in user_list:
            User.model_validate(user)

    def test_users_no_duplicates(self, users):
        user_ids = [user["id"] for user in users["items"]]
        assert len(user_ids) == len(set(user_ids))

    @pytest.mark.parametrize("user_id", [1, 6, 12])
    def test_user(self, app_url, user_id):
        response = requests.get(f"""{app_url}{Urls().api_url("users")}{user_id}""")
        assert response.status_code == HTTPStatus.OK

        user = response.json()
        User.model_validate(user)

    @pytest.mark.parametrize("user_id", [123, 999])
    def test_user_nonexistent_ids(self, app_url, user_id):
        response = requests.get(f"""{app_url}{Urls().api_url("users")}{user_id}""")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["detail"] == "User not found"

    @pytest.mark.parametrize("user_id", ["ddsf"])
    def test_user_invalid_type_ids(self, app_url, user_id):
        response = requests.get(f"""{app_url}{Urls().api_url("users")}{user_id}""")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("user_id", [0, -1])
    def test_user_invalid_ids(self, app_url, user_id):
        response = requests.get(f"""{app_url}{Urls().api_url("users")}{user_id}""")
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["detail"] == "User ID is invalid"

    def test_get_user(self, app_url, post_delete_user, test_data):
        response = requests.get(f"""{app_url}{Urls().api_url("users")}{post_delete_user['id']}""")

        assert response.status_code == HTTPStatus.OK
        assert response.json()["id"] == post_delete_user["id"]
        assert response.json()["name"] == post_delete_user["name"]
        assert response.json()["email"] == post_delete_user["email"]

    def test_post_user(self, app_url, test_data):
        users_before = requests.get(f"""{app_url}{Urls().api_url("users")}""").json()["items"]

        user_data = test_data.get_test_user_data()
        response = requests.post(f"""{app_url}{Urls().api_url("users")}""", json=user_data)
        assert response.status_code == HTTPStatus.CREATED

        users_after = requests.get(f"""{app_url}{Urls().api_url("users")}""").json()["items"]
        assert len(users_after) == len(users_before) + 1

        created_user = list(filter(lambda x: x["name"] == user_data["name"], users_after))

        assert created_user[0]["name"] == user_data["name"]
        assert created_user[0]["email"] == user_data["email"]

        # удаление созданной в тесте записи
        response = requests.delete(f"""{app_url}{Urls().api_url("users")}{created_user[0]["id"]}""", data={})
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_update_user(self, app_url, post_delete_user, test_data):
        user_before = post_delete_user
        updated_user_data = test_data.get_test_user_data_for_update()
        response = requests.put(f"""{app_url}{Urls().api_url("users")}{post_delete_user['id']}""",
                                json=updated_user_data)
        assert response.status_code == HTTPStatus.NO_CONTENT

        response = requests.get(f"""{app_url}{Urls().api_url("users")}{post_delete_user['id']}""")

        assert user_before["id"] == response.json()["id"]
        assert user_before["name"] != response.json()["name"]
        assert user_before["email"] != response.json()["email"]

        assert response.json()["id"] == user_before["id"]
        assert response.json()["name"] == updated_user_data["name"]
        assert response.json()["email"] == updated_user_data["email"]

    def test_delete_user(self, app_url, created_user):
        users_before = requests.get(f"""{app_url}{Urls().api_url("users")}""").json()["items"]
        response = requests.delete(f"""{app_url}{Urls().api_url("users")}{created_user['id']}""", data={})

        assert response.status_code == HTTPStatus.NO_CONTENT

        users_after = requests.get(f"""{app_url}{Urls().api_url("users")}""").json()["items"]

        assert len(users_after) == len(users_before) - 1
