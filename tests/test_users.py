from http import HTTPStatus

import pytest
import requests

from reqres_app.models.error_message_model import BasicErrorResponse, ErrorResponse
from reqres_app.models.user_model import User, UserResponse
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

    @pytest.mark.parametrize("user_id", [12399, 99999])
    def test_user_nonexistent_ids(self, user_id):
        response = requests.get(f"{Urls().api_url('users')}{user_id}")
        message = BasicErrorResponse.model_validate(response.json())

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert message.detail == UserData.USER_NOT_FOUND

    @pytest.mark.parametrize("user_id", ["ddsf"])
    def test_user_invalid_type_ids(self, user_id):
        response = requests.get(f"{Urls().api_url('users')}{user_id}")
        message = ErrorResponse.model_validate(response.json())
        error_detail = message.detail[0]

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert error_detail.msg == UserData.INVALID_USER_ID_TYPE
        assert error_detail.input == user_id

    @pytest.mark.parametrize("user_id", [0, -1])
    def test_user_invalid_ids(self, user_id):
        response = requests.get(f"{Urls().api_url('users')}{user_id}")
        message = BasicErrorResponse.model_validate(response.json())

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert message.detail == UserData.INVALID_USER_ID

    def test_post_user(self, test_data):
        user_data = test_data.get_test_user_data()
        response = requests.post(Urls().api_url("users"), json=user_data)
        assert response.status_code == HTTPStatus.CREATED

        user = requests.get(f"{Urls().api_url('users')}{response.json()['id']}").json()
        created_user_model = UserResponse.model_validate(user)

        assert created_user_model.id == response.json()["id"]
        assert created_user_model.email == user_data["email"]
        assert created_user_model.first_name == user_data["first_name"]
        assert created_user_model.last_name == user_data["last_name"]
        assert created_user_model.avatar == user_data["avatar"]

        # удаление созданной в тесте записи
        response = requests.delete(f"{Urls().api_url('users')}{response.json()['id']}", data={})
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_update_user(self, fill_test_data, test_data):
        user_id = fill_test_data[0]
        user_before_response = requests.get(f"{Urls().api_url('users')}{user_id}").json()
        user_before = UserResponse.model_validate(user_before_response)
        updated_user_data = test_data.get_test_user_data_for_update()
        response = requests.patch(f"{Urls().api_url('users')}{user_id}", json=updated_user_data)
        assert response.status_code == HTTPStatus.OK

        user_after = requests.get(f"{Urls().api_url('users')}{user_id}").json()
        updated_user = UserResponse.model_validate(user_after)

        assert user_before.id == updated_user.id
        assert user_before.email != updated_user.email
        assert user_before.first_name != updated_user.first_name
        assert user_before.last_name != updated_user.last_name
        assert user_before.avatar != updated_user.avatar

        assert updated_user.email == updated_user_data["email"]
        assert updated_user.first_name == updated_user_data["first_name"]
        assert updated_user.last_name == updated_user_data["last_name"]
        assert updated_user.avatar == updated_user_data["avatar"]

    def test_update_user_method_not_allowed(self):
        response = requests.put(Urls().api_url("users"))
        message = BasicErrorResponse.model_validate(response.json())
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        assert message.detail == UserData.METHOD_NOT_ALLOWED

    def test_update_user_405(self, test_data):
        update_data = test_data.get_test_user_data_for_update()
        str_value = "ffdsf"
        response = requests.patch(f"{Urls().api_url('users')}{str_value}", data=update_data)
        message = ErrorResponse.model_validate(response.json())
        error_detail = message.detail[0]

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

        assert error_detail.msg == UserData.INVALID_USER_ID_TYPE
        assert error_detail.input == str_value

    def test_delete_user(self, fill_test_data):
        user_id_for_delete = fill_test_data[0]
        response = requests.delete(f"{Urls().api_url('users')}{user_id_for_delete}", data={})

        assert response.status_code == HTTPStatus.NO_CONTENT

        deleted_user_response = requests.get(f"{Urls().api_url('users')}{user_id_for_delete}")

        deleted_user = BasicErrorResponse.model_validate(deleted_user_response.json())

        assert deleted_user_response.status_code == HTTPStatus.NOT_FOUND
        assert deleted_user.detail == UserData.USER_NOT_FOUND

    @pytest.mark.parametrize(
        ["user_id", "status_code", "detail"],
        [[-1, HTTPStatus.BAD_REQUEST, "User ID is invalid"], [99999, HTTPStatus.NOT_FOUND, "User not found"]],
    )
    def test_delete_user_negative(self, user_id, status_code, detail):
        response = requests.delete(f"{Urls().api_url('users')}{user_id}", data={})
        message = BasicErrorResponse.model_validate(response.json())

        assert response.status_code == status_code
        assert message.detail == detail

    def test_delete_user_405(self):
        str_value = "ffdsf"
        response = requests.delete(f"{Urls().api_url('users')}{str_value}", data={})
        message = ErrorResponse.model_validate(response.json())
        error_detail = message.detail[0]

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert error_detail.msg == UserData.INVALID_USER_ID_TYPE
        assert error_detail.input == str_value
