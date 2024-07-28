from http import HTTPStatus

import pytest
import requests

from reqres_tests.utils.urls import Urls
from reqres_tests.data.pagination_data import PaginationData


class TestPagination:
    def test_get_users_pagination(self, app_url):
        response = requests.get(f"""{app_url}{Urls().api_url("users")}""")
        assert response.status_code == HTTPStatus.OK

        response_json = response.json()
        assert PaginationData.PAGE in response_json
        assert PaginationData.PAGES in response_json
        assert PaginationData.SIZE in response_json
        assert PaginationData.TOTAL in response_json

    @pytest.mark.parametrize("size", [2, 4, 8])
    def test_get_users_pagination_size(self, app_url, size):
        response = requests.get(f"""{app_url}{Urls().api_url("users")}?size={size}""")
        assert response.status_code == HTTPStatus.OK
        response_json = response.json()
        assert len(response_json["items"]) == size

    def test_get_users_pagination_page(self, app_url):
        response = requests.get(f"""{app_url}{Urls().api_url("users")}?page=2""")
        assert response.status_code == HTTPStatus.OK
        response_json = response.json()
        assert response_json["page"] == 2

    @pytest.mark.parametrize(["size", "page"], [[2, 6], [4, 1], [3, 3]])
    def test_get_users_pagination_size_and_page(self, app_url, size, page):
        response = requests.get(f"""{app_url}{Urls().api_url("users")}?size={size}&page={page}""")
        assert response.status_code == HTTPStatus.OK
        response_json = response.json()
        assert len(response_json["items"]) == size
        assert response_json["page"] == page

    @pytest.mark.parametrize(["size", "exp_msg"],
                             [[-1, PaginationData.INVALID_INPUT_MSG], ["ffdsf", PaginationData.INVALID_INT_INPUT_MSG]])
    def test_get_users_pagination_invalid_size(self, app_url, size, exp_msg):
        response = requests.get(f"""{app_url}{Urls().api_url("users")}?size={size}""")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert PaginationData.SIZE in response.json()["detail"][0]["loc"]
        assert response.json()["detail"][0]["msg"] == exp_msg

    @pytest.mark.parametrize(["page", "exp_msg"],
                             [[-1, PaginationData.INVALID_INPUT_MSG], ["ffdsf", PaginationData.INVALID_INT_INPUT_MSG]])
    def test_get_users_pagination_invalid_page(self, app_url, page, exp_msg):
        response = requests.get(f"""{app_url}{Urls().api_url("users")}?page={page}""")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert PaginationData.PAGE in response.json()["detail"][0]["loc"]
        assert response.json()["detail"][0]["msg"] == exp_msg
