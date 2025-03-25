import json
import logging
from http import HTTPStatus
from pathlib import Path

import pytest
import requests

from app.models.User import User


@pytest.mark.usefixtures("app_url")
class TestUsersSmoke:

    FILE_PATH = "../../users.json"

    def test_status_check_users_exist(self, app_url):
        data: list[User]
        resp_status = requests.get(f"{app_url}/status")
        assert resp_status.status_code == HTTPStatus.OK

    def test_smoke_users(self, app_url: str):
        response = requests.get(f"{app_url}/users")
        assert response.status_code == HTTPStatus.OK
        result = response.json()
        assert "items" in result
        assert isinstance(result["items"], list)
