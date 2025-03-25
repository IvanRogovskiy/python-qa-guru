
from fastapi import APIRouter

from app.database.engine import check_database
from app.models.AppStatus import AppStatus

status_router = APIRouter()


@status_router.get("/api/status")
def get_app_status() -> AppStatus:
    return AppStatus(database=check_database())
