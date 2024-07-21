from config import API_USERS_URL


class TestApi:
    def test_get_users(self, client):
        response = client.get(API_USERS_URL)
        assert response.status_code == 200

    def test_create_user(self, client, test_data):
        users_before = client.get(API_USERS_URL).json()

        user_data = test_data.get_test_user_data()
        response = client.post(API_USERS_URL, json=user_data)
        assert response.status_code == 200

        users_after = client.get(API_USERS_URL).json()
        assert len(users_after) == len(users_before) + 1

        created_user = list(filter(lambda x: x["name"] == user_data["name"], users_after))

        assert created_user[0]["name"] == user_data["name"]
        assert created_user[0]["email"] == user_data["email"]

    def test_get_user(self, client, created_user, test_data):
        response = client.get(f"{API_USERS_URL}{created_user['id']}")

        assert response.status_code == 200
        assert response.json()["id"] == created_user["id"]
        assert response.json()["name"] == created_user["name"]
        assert response.json()["email"] == created_user["email"]

    def test_update_user(self, client, created_user, test_data):
        user_before = created_user
        updated_user_data = test_data.get_test_user_data_for_update()
        response = client.put(f"{API_USERS_URL}{created_user['id']}", json=updated_user_data)

        assert response.status_code == 200
        assert user_before["id"] == response.json()["id"]
        assert user_before["name"] != response.json()["name"]
        assert user_before["email"] != response.json()["email"]

        assert response.json()["id"] == user_before["id"]
        assert response.json()["name"] == updated_user_data["name"]
        assert response.json()["email"] == updated_user_data["email"]

    def test_delete_user(self, client, created_user):
        users_before = client.get(API_USERS_URL).json()

        response = client.delete(f"{API_USERS_URL}{created_user['id']}")

        assert response.status_code == 200
        assert response.json()["message"] == "User deleted"

        users_after = client.get(API_USERS_URL).json()

        assert len(users_after) == len(users_before) - 1
