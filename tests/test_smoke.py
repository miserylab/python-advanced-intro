from http import HTTPStatus

import pytest
import requests

from reqres_tests.data.root_data import RootData
from reqres_tests.utils.urls import Urls


class TestSmoke:
    def test_root(self, app_url):
        response = requests.get(app_url)
        assert response.status_code == HTTPStatus.OK
        assert response.json()["message"] == RootData.MSG

    def test_status(self):
        response = requests.get(Urls().api_url("status"))
        assert response.status_code == HTTPStatus.OK
        assert response.json()["database"] is True

    @pytest.mark.usefixtures("fill_test_data")
    def test_get_users(self):
        response = requests.get(Urls().api_url("users"))
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(), dict)
