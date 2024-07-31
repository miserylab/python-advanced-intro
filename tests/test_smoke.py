from http import HTTPStatus

import pytest
import requests

from reqres_app.models.app_status import AppStatus
from reqres_app.models.root_model import Root
from reqres_tests.data.root_data import RootData
from reqres_tests.utils.urls import Urls


class TestSmoke:
    def test_root(self, app_url):
        response = requests.get(app_url)
        assert response.status_code == HTTPStatus.OK

        root_msg = Root.model_validate(response.json())

        assert root_msg.message == RootData.MSG

    def test_status(self):
        response = requests.get(Urls().api_url("status"))
        assert response.status_code == HTTPStatus.OK

        status = AppStatus.model_validate(response.json())

        assert status.database is True

    @pytest.mark.usefixtures("fill_test_data")
    def test_get_users(self):
        response = requests.get(Urls().api_url("users"))
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(), dict)
