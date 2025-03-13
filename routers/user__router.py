import json
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from models.User import User

# import app from app

user_router = APIRouter()


@user_router.post("/api/users")
def create_user(user: User):
    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }
    with open('users.json', 'r') as file:
        data = json.load(file)
        for d in data:
            if d["id"] == user.id:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"User with id: {user.id} already exist")
        data.append(user_dict)
    with open('users.json', 'w') as file:
        json.dump(data, file)


@user_router.get("/api/users/{user_id}", response_model=User)
def get_user(user_id: int) -> User:
    if user_id < 0:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    with open('users.json', 'r') as file:
        data = json.load(file)
        for user in data:
            if user["id"] == user_id:
                return User(email=user["email"], name=user["name"], id=user["id"])
    raise HTTPException(status_code=404, detail="User not found")


@user_router.delete("/api/users/{user_id}")
def delete_user(user_id: int) -> int:
    with open('users.json', 'r') as file:
        data = json.load(file)
        for user in data:
            if user["id"] == user_id:
                data.remove(user)
                with open('users.json', 'w') as file:
                    json.dump(data, file)
                return user_id
        raise HTTPException(status_code=404, detail="User not found")



