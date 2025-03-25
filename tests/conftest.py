import os
import random
from http import HTTPStatus

import dotenv
import pytest
import requests
from faker import Faker

from app.models.User import UserCreate
from tests.utils.data_generator import generate_random_user


@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    print("Настройка фикстуры")
    return os.getenv("BASE_URL")


@pytest.fixture()
def fill_test_users(app_url):
    api_users = []
    for i in range(0, 12):
        new_user = generate_random_user()
        api_users.append(new_user)
    user_ids = [user.id for user in api_users]

    yield user_ids

    for user_id in user_ids:
        resp = requests.delete(f"{app_url}/users/{user_id}")
        assert resp.status_code == HTTPStatus.OK


@pytest.fixture()
def random_user():
    faker = Faker()
    email = faker.email(domain="qaguru.autotest")
    name = faker.name()
    return UserCreate(email=email, name=name)


# @pytest.fixture()
# def user(app_url, random_user) -> User:
#     user: UserCreate = random_user
#     response = requests.post(f"{app_url}/users", json=user.model_dump(include={"name", "email"}))
#     assert response.status_code == HTTPStatus.CREATED
#     return User(**response.json())


# @pytest.fixture(scope="module")
@pytest.fixture()
def users(app_url, random_user):
    users = []
    for i in range(0, 12):
        user = random_user
        response = requests.post(f"{app_url}/users", json=user.model_dump(include={"name", "email"}))
        assert response.status_code == HTTPStatus.CREATED
        users.append(response.json())
    user_ids: list[int] = [user["id"] for user in users]

    yield user_ids

    for user_id in user_ids:
        requests.delete(f"{app_url}/api/users/{user_id}")


@pytest.fixture()
def pagination_test_data(fill_test_users) -> list[tuple]:
    res: list[tuple] = []
    users_for_test = fill_test_users
    users_count = len(users_for_test)
    size = random.randint(1, users_count)
    # res.append((users_count, 1))
    # res.append((1, users_count))
    res.append((size, (users_count + size - 1) // size))
    return res
