import json
import os
import random

import dotenv
import pytest

from tests.utils.data_generator import generate_random_user


@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture()
def app_url():
    return os.getenv("BASE_URL")


# @pytest.fixture()
# def pagination_test_data() -> list[tuple]:
#     res: list[tuple] = []
#     new_users: list[dict] = []
#     with open('../../users.json', 'r') as f:
#         data = json.load(f)
#     if len(data) < 10:
#         for i in range(0, 10 - len(data)):
#             user: dict = dict(vars(generate_random_user()))
#             new_users.append(user)
#         with open('users.json', 'w') as f:
#             for u in new_users:
#                 json.dump(u, f)
#     users_count = len(data)
#     size = random.randint(1, users_count)
#     # res.append((users_count, 1))
#     # res.append((1, users_count))
#     res.append((size, (users_count + size - 1) // size))
#     return res
