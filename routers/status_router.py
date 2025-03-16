import json

from fastapi import APIRouter

from models.AppStatus import AppStatus

status_router = APIRouter()


@status_router.get("/api/status")
def get_app_status() -> AppStatus:
    with open('users.json', 'r') as file:
        data = json.load(file)
    return AppStatus(users=bool(data))
