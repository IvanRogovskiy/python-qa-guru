import json
import logging
from http import HTTPStatus
from pathlib import Path

import pytest
import requests

from models.User import User


@pytest.mark.usefixtures("app_url")
class TestUsersSmoke:

    FILE_PATH = "../../users.json"

    def test_status_check_users_exist(self, app_url):
        data: list[User]
        with open(self.FILE_PATH, 'r') as file:
            data = json.load(file)

        if data:
            resp_status = requests.get(f"{app_url}/status")
            assert resp_status.status_code == HTTPStatus.OK
            assert resp_status.json()["users"]
        else:
            logging.error("Отсуствуют пользователи")

    def test_status_check_users_empty(self, app_url):
        data: list[User]
        Path.home()
        with open(self.FILE_PATH, 'r') as file:
            data = json.load(file)
        with open(self.FILE_PATH, "w") as file:
            file.truncate()
            json.dump([], file)

        if not data:
            resp_status = requests.get(f"{app_url}/status")
            assert resp_status.status_code == HTTPStatus.OK
            assert not resp_status.json()["users"]
        else:
            logging.error("Пользователи существуют, необходимо очистить")
        with open(self.FILE_PATH, "w") as file:
            json.dump(data, file)
