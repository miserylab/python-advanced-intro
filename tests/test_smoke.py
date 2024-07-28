from http import HTTPStatus

import requests

from reqres_tests.data.root_data import RootData
from reqres_tests.utils.urls import Urls


class TestSmoke:
    def test_root(self, app_url):
        response = requests.get(f"""{app_url}/""")
        assert response.status_code == HTTPStatus.OK
        assert response.json()["message"] == RootData.MSG

    def test_status(self, app_url):
        response = requests.get(f"""{app_url}{Urls().api_url("status")}""")
        assert response.status_code == HTTPStatus.OK
        assert response.json()["users"] is True

    def test_get_users(self, app_url):
        response = requests.get(f"""{app_url}{Urls().api_url("users")}""")
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(), dict)
