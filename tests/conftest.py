import pytest
from fastapi.testclient import TestClient

from reqres_app.api import app
from reqres_tests.utils.utils import TestData


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_data():
    return TestData()


@pytest.fixture
def created_user(client, test_data):
    user_data = test_data.get_test_user_data()
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 200
    return response.json()
