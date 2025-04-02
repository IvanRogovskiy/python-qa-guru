import json
import os
from http import HTTPStatus

import pytest
import requests
from faker import Faker
import random

from app.models.User import User, UserCreate

faker = Faker()


def generate_random_user() -> User:
    email = faker.email(domain="qaguru.autotest")
    name = faker.name()
    user = UserCreate(email=email, name=name)
    response = requests.post(f"{os.getenv('BASE_URL')}/users", json=user.model_dump(include={"name", "email"}))
    assert response.status_code == HTTPStatus.CREATED
    return User(**response.json())
