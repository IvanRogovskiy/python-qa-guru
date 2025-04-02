import random
from http import HTTPStatus

import pytest
import requests
from faker import Faker

from tests.utils.data_generator import generate_random_user
from app.models.User import User


class TestUsers:

    def test_post_user(self, app_url):
        random_user = generate_random_user()
        body = {
            "name": random_user.name,
            "email": random_user.email,
        }
        resp_create_user = requests.post(f"{app_url}/users", json=body)
        User.model_validate(resp_create_user.json())
        assert resp_create_user.status_code == HTTPStatus.CREATED
        resp_get_user = requests.get(f"{app_url}/users/{resp_create_user.json()['id']}")
        assert resp_get_user.status_code == 200
        assert resp_get_user.json()["name"] == random_user.name
        assert resp_get_user.json()["email"] == random_user.email

    @pytest.mark.parametrize("name, email", [
        ("Ivan Ptushkin", "ivapt.ru")
    ])
    def test_post_user_invalid_email(self, app_url, name, email):
        body = {
            "name": name,
            "email": email,
        }
        resp_create_user = requests.post(f"{app_url}/users", json=body)
        assert resp_create_user.status_code == 400
        assert "An email address must have an @-sign" in resp_create_user.json()["detail"]

    def test_patch_user(self, app_url, new_user):
        faker = Faker()
        body = {
            "name": faker.name(),
            "email": new_user.email
        }
        resp_patch_user = requests.patch(f"{app_url}/users/{new_user.id}", json=body)
        User.model_validate(resp_patch_user.json())
        assert resp_patch_user.status_code == HTTPStatus.OK
        resp_get_user = requests.get(f"{app_url}/users/{new_user.id}")
        assert resp_get_user.status_code == 200
        body["id"] = new_user.id
        assert resp_get_user.json() == body

    def test_patch_user_fail_to_change_id(self, app_url, new_user, existing_user_id):
        body = {
            "name": new_user.name,
            "email": new_user.email,
            "id": existing_user_id
        }
        resp_patch_user = requests.patch(f"{app_url}/users/{new_user.id}", json=body)
        assert resp_patch_user.status_code == HTTPStatus.OK
        resp_get_user = requests.get(f"{app_url}/users/{new_user.id}")
        assert resp_get_user.status_code == 200
        resp_get_user.json()["id"] = new_user.id

    def test_delete_user(self, app_url, new_user):
        resp_delete_user = requests.delete(f"{app_url}/users/{new_user.id}")
        assert resp_delete_user.status_code == 200
        resp_get_user = requests.get(f"{app_url}/users/{new_user.id}")
        assert resp_get_user.status_code == 404
        assert resp_get_user.json()["detail"] == "User not found"

    @pytest.mark.parametrize("user_id", [5000])
    def test_delete_user_with_not_exist_id(self, app_url, user_id):
        resp_delete_user = requests.delete(f"{app_url}/users/{user_id}")
        assert resp_delete_user.status_code == 404
        assert resp_delete_user.json()["detail"] == f"User with id {user_id} not found"


