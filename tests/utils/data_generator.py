import json
from faker import Faker
import random

from models.User import User

faker = Faker()


def generate_random_user() -> User:
    with open('users.json', 'r') as file:
        data = json.load(file)
    email = faker.email(domain="qaguru.autotest")
    name = faker.name()
    user_id: int = 1
    while any(d.get("id") == user_id for d in data):
        user_id = random.randint(0, 1000)
    return User(email=email, name=name, id=user_id)