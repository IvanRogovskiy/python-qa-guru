import random

import pytest
import requests


@pytest.mark.usefixtures("app_url")
class TestUsersCrud:

    @pytest.mark.parametrize("name, email, id", [
        ("Ivan Ptushkin", "ivapt@mail.ru", 7)
    ])
    def test_post_user(self, app_url, name, email, id):
        body = {
            "name": name,
            "email": email,
            "id": id
        }
        resp_create_user = requests.post(f"{app_url}/users", json=body)
        assert resp_create_user.status_code == 200
        resp_get_user = requests.get(f"{app_url}/users/{id}")
        assert resp_get_user.status_code == 200
        assert resp_get_user.json()

    @pytest.mark.parametrize("name, email, id", [
        ("Ivan Ptushkin", "ivapt@mail.ru", "one")
    ])
    def test_post_user_invalid_id(self, app_url, name, email, id):
        body = {
            "name": name,
            "email": email,
            "id": id
        }
        resp_create_user = requests.post(f"{app_url}/users", json=body)
        assert resp_create_user.status_code == 400
        assert resp_create_user.json()["detail"] == "Validation error"

    @pytest.mark.parametrize("name, email, id", [
        ("Ivan Ptushkin", "ivapt@mail.ru", "one")
    ])
    def test_post_user_no_id(self, app_url, name, email, id):
        body = {
            "name": name,
            "email": email,
        }
        resp_create_user = requests.post(f"{app_url}/users", json=body)
        assert resp_create_user.status_code == 400
        assert resp_create_user.json()["detail"] == "Validation error"

    @pytest.mark.parametrize("user_id", [55])
    def test_delete_user(self, app_url, user_id):
        body = {
            "name": "Petr Van",
            "email": "petya_van@mail.ru",
            "id": user_id
        }
        requests.post(f"{app_url}/users", json=body)
        resp_delete_user = requests.delete(f"{app_url}/users/{user_id}")
        assert resp_delete_user.status_code == 200
        resp_get_user = requests.get(f"{app_url}/users/{user_id}")
        assert resp_get_user.status_code == 404
        assert resp_get_user.json()["detail"] == "User not found"

    @pytest.mark.parametrize("user_id", [123])
    def test_delete_user_id_not_exist(self, user_id, app_url):
        body = {
            "name": "Petr Van",
            "email": "petya_van@mail.ru",
            "id": user_id
        }
        requests.post(f"{app_url}/users", json=body)
        resp_delete_user = requests.delete(f"{app_url}/users/{321}")
        assert resp_delete_user.status_code == 404
        assert resp_delete_user.json()["detail"] == "User not found"

    def test_delete_user_id_already_exist(self, app_url):
        user_id: int = 7
        body = {
            "name": "Petr Van",
            "email": "petya_van@mail.ru",
            "id": user_id
        }
        while requests.post(f"{app_url}/users", json=body).status_code != 200:
            user_id = random.randint(0, 1000)
            body["id"] = user_id
        resp_post_user = requests.post(f"{app_url}/users", json=body)
        assert resp_post_user.status_code == 400
        assert resp_post_user.json()["detail"] == f"User with id: {user_id} already exist"
