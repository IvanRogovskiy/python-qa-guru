import random

import pytest
import requests
from http import HTTPStatus

from app.models.User import User


@pytest.mark.usefixtures("app_url")
class TestUsersPagination:
    def test_users_pagination_size(self, app_url):
        params: dict = {
            "page": 1,
            "size": 5
        }
        resp_get_user_with_page = requests.get(f"{app_url}/users", params=params)
        assert resp_get_user_with_page.status_code == HTTPStatus.OK
        assert len(resp_get_user_with_page.json()) == 5

    @pytest.mark.usefixtures("pagination_test_data")
    def test_users_pagination_page_count(self, app_url: str, pagination_test_data):
        for d in pagination_test_data:
            size = d[0]
            page_count = d[1]
            data: list[User]
            for page in range(1, page_count + 2):
                params: dict = {
                    "page": page,
                    "size": size
                }
                resp_get_user_with_page = requests.get(f"{app_url}/users", params=params)
                print(resp_get_user_with_page.url)
                if page == page_count + 1:
                    assert resp_get_user_with_page.json()["items"] == []
                else:
                    assert resp_get_user_with_page.status_code == HTTPStatus.OK
                    assert resp_get_user_with_page.json()["pages"] == page_count

    def test_users_pagination_unique_data(self, app_url):
        page = 1
        all_items = set()
        while True:
            params: dict = {
                "page": page,
                "size": 6
            }
            resp_get_user_with_page = requests.get(f"{app_url}/users", params=params)
            assert resp_get_user_with_page.status_code == HTTPStatus.OK
            data = resp_get_user_with_page.json()["items"]
            if not data:
                break
            new_item = set(u["id"] for u in data)
            assert not (new_item & all_items)
            all_items |= new_item
            page += 1
