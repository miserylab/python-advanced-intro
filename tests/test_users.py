from http import HTTPStatus

import pytest
import requests

from reqres_app.models.user_model import User
from reqres_tests.data.user_data import UserData
from reqres_tests.utils.urls import Urls


class TestApi:
    @pytest.mark.usefixtures("fill_test_data")
    def test_users(self):
        response = requests.get(Urls().api_url("users"))
        assert response.status_code == HTTPStatus.OK

        user_list = response.json()["items"]
        for user in user_list:
            User.model_validate(user)

    @pytest.mark.usefixtures("fill_test_data")
    def test_users_no_duplicates(self, users):
        user_ids = [user["id"] for user in users["items"]]
        assert len(user_ids) == len(set(user_ids))

    def test_user(self, fill_test_data):
        for user_id in fill_test_data:
            response = requests.get(f"{Urls().api_url('users')}{user_id}")
            assert response.status_code == HTTPStatus.OK

            user = response.json()
            User.model_validate(user)

    @pytest.mark.parametrize("user_id", [123, 999])
    def test_user_nonexistent_ids(self, user_id):
        response = requests.get(f"{Urls().api_url('users')}{user_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["detail"] == UserData.USER_NOT_FOUND

    @pytest.mark.parametrize("user_id", ["ddsf"])
    def test_user_invalid_type_ids(self, user_id):
        response = requests.get(f"{Urls().api_url('users')}{user_id}")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("user_id", [0, -1])
    def test_user_invalid_ids(self, user_id):
        response = requests.get(f"{Urls().api_url('users')}{user_id}")
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["detail"] == UserData.INVALID_USER_ID

    def test_get_user(self, post_delete_user, test_data):
        response = requests.get(f"{Urls().api_url('users')}{post_delete_user['id']}")

        assert response.status_code == HTTPStatus.OK
        assert response.json()["id"] == post_delete_user["id"]
        assert response.json()["email"] == post_delete_user["email"]
        assert response.json()["first_name"] == post_delete_user["first_name"]
        assert response.json()["last_name"] == post_delete_user["last_name"]
        assert response.json()["avatar"] == post_delete_user["avatar"]

    def test_post_user(self, test_data):
        users_before = requests.get(Urls().api_url("users")).json()["items"]

        user_data = test_data.get_test_user_data()
        response = requests.post(Urls().api_url("users"), json=user_data)
        assert response.status_code == HTTPStatus.CREATED

        users_after = requests.get(Urls().api_url("users")).json()["items"]
        assert len(users_after) == len(users_before) + 1

        created_user = list(filter(lambda x: x["last_name"] == user_data["last_name"], users_after))

        assert created_user[0]["email"] == user_data["email"]
        assert created_user[0]["first_name"] == user_data["first_name"]
        assert created_user[0]["last_name"] == user_data["last_name"]
        assert created_user[0]["avatar"] == user_data["avatar"]

        # удаление созданной в тесте записи
        response = requests.delete(f"{Urls().api_url('users')}{created_user[0]['id']}", data={})
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_update_user(self, post_delete_user, test_data):
        user_before = post_delete_user
        updated_user_data = test_data.get_test_user_data_for_update()
        response = requests.patch(f"{Urls().api_url('users')}{post_delete_user['id']}", json=updated_user_data)
        assert response.status_code == HTTPStatus.OK

        user_after = requests.get(f"{Urls().api_url('users')}{post_delete_user['id']}").json()

        assert user_before["id"] == user_after["id"]
        assert user_before["email"] != user_after["email"]
        assert user_before["first_name"] != user_after["first_name"]
        assert user_before["last_name"] != user_after["last_name"]
        assert user_before["avatar"] != user_after["avatar"]

        assert user_after["email"] == updated_user_data["email"]
        assert user_after["first_name"] == updated_user_data["first_name"]
        assert user_after["last_name"] == updated_user_data["last_name"]
        assert user_after["avatar"] == updated_user_data["avatar"]

    def test_update_user_method_not_allowed(self, app_url):
        response = requests.put(Urls().api_url("users"))
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_update_user_405(self, test_data):
        update_data = test_data.get_test_user_data_for_update()
        str_value = "ffdsf"
        response = requests.patch(f"{Urls().api_url('users')}{str_value}", data=update_data)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["msg"] == UserData.INVALID_USER_ID_TYPE
        assert response.json()["detail"][0]["input"] == str_value

    def test_delete_user(self, created_user):
        users_before = requests.get(Urls().api_url("users")).json()["items"]
        response = requests.delete(f"{Urls().api_url('users')}{created_user['id']}", data={})

        assert response.status_code == HTTPStatus.NO_CONTENT

        users_after = requests.get(Urls().api_url("users")).json()["items"]

        assert len(users_after) == len(users_before) - 1

    @pytest.mark.parametrize(
        ["user_id", "status_code", "detail"],
        [[-1, HTTPStatus.BAD_REQUEST, "User ID is invalid"], [99999, HTTPStatus.NOT_FOUND, "User not found"]],
    )
    def test_delete_user_negative(self, app_url, user_id, status_code, detail):
        response = requests.delete(f"{Urls().api_url('users')}{user_id}", data={})

        assert response.status_code == status_code
        assert response.json()["detail"] == detail

    def test_delete_user_405(self):
        str_value = "ffdsf"
        response = requests.delete(f"{Urls().api_url('users')}{str_value}", data={})

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["msg"] == UserData.INVALID_USER_ID_TYPE
        assert response.json()["detail"][0]["input"] == str_value
