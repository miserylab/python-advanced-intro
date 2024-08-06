from http import HTTPStatus

import pytest
import requests

from app.models.error_message_model import ErrorResponse
from app.models.pagination_model import PaginationResponse
from app_tests.data.pagination_data import PaginationData
from app_tests.utils.urls import Urls
from app_tests.utils.utils import Utils


@pytest.fixture
def total_users():
    return len(requests.get(Urls().api_url("users")).json()["items"])


@pytest.mark.usefixtures("fill_test_data")
class TestPagination:
    def test_get_users_pagination(self, total_users):
        response = requests.get(Urls().api_url("users"))
        assert response.status_code == HTTPStatus.OK

        pagination = PaginationResponse.model_validate(response.json())

        assert pagination.total == total_users
        assert pagination.page == 1
        assert pagination.size == PaginationData.DEFAULT_SIZE
        assert pagination.pages == Utils.get_pages_in_pagination(response.json()["total"], response.json()["size"])

    @pytest.mark.parametrize("size", [2, 4, 8])
    def test_get_users_pagination_size(self, size, total_users):
        response = requests.get(f"{Urls().api_url('users')}?size={size}")
        assert response.status_code == HTTPStatus.OK

        pagination = PaginationResponse.model_validate(response.json())

        assert len(pagination.items) == size
        assert pagination.total == total_users
        assert pagination.page == 1
        assert pagination.size == size
        assert pagination.pages == Utils.get_pages_in_pagination(response.json()["total"], response.json()["size"])

    def test_get_users_pagination_page(self, total_users):
        response = requests.get(f"{Urls().api_url('users')}?page=2")
        assert response.status_code == HTTPStatus.OK

        pagination = PaginationResponse.model_validate(response.json())

        assert pagination.total == total_users
        assert pagination.page == 2
        assert pagination.size == PaginationData.DEFAULT_SIZE
        assert pagination.pages == Utils.get_pages_in_pagination(response.json()["total"], response.json()["size"])

    @pytest.mark.parametrize(["size", "page"], [[2, 6], [4, 1], [3, 3]])
    def test_get_users_pagination_size_and_page(self, size, page, total_users):
        response = requests.get(f"{Urls().api_url('users')}?size={size}&page={page}")
        assert response.status_code == HTTPStatus.OK

        pagination = PaginationResponse.model_validate(response.json())

        assert len(pagination.items) == size
        assert pagination.total == total_users
        assert pagination.page == page
        assert pagination.size == size
        assert pagination.pages == Utils.get_pages_in_pagination(response.json()["total"], response.json()["size"])

    @pytest.mark.parametrize(
        ["size", "exp_msg"], [[-1, PaginationData.INVALID_INPUT_MSG], ["ffdsf", PaginationData.INVALID_INT_INPUT_MSG]]
    )
    def test_get_users_pagination_invalid_size(self, size, exp_msg):
        response = requests.get(f"{Urls().api_url('users')}?size={size}")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

        message = ErrorResponse.model_validate(response.json())
        error_detail = message.detail[0]

        assert PaginationData.SIZE in error_detail.loc
        assert error_detail.msg == exp_msg

    @pytest.mark.parametrize(
        ["page", "exp_msg"], [[-1, PaginationData.INVALID_INPUT_MSG], ["ffdsf", PaginationData.INVALID_INT_INPUT_MSG]]
    )
    def test_get_users_pagination_invalid_page(self, page, exp_msg):
        response = requests.get(f"{Urls().api_url('users')}?page={page}")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

        message = ErrorResponse.model_validate(response.json())
        error_detail = message.detail[0]

        assert PaginationData.PAGE in error_detail.loc
        assert error_detail.msg == exp_msg

    def test_get_users_pagination_entries_on_pages(self, total_users):
        total = total_users
        size = total // 2
        items_on_first_page = requests.get(f"{Urls().api_url('users')}?size={size}&page=1").json()["items"]
        ids_on_first_page = [item["id"] for item in items_on_first_page]

        items_on_second_page = requests.get(f"{Urls().api_url('users')}?size={size}&page=2").json()["items"]
        ids_on_second_page = [item["id"] for item in items_on_second_page]

        assert sorted(ids_on_first_page) != sorted(ids_on_second_page)
