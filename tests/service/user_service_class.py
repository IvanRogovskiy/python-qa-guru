from http import HTTPStatus

from tests.sessions.base_session_class import UserSession
from tests.models.ResponseGetUser import ResponseGetUser


class UserService:
    def __init__(self, app_url):
        self.session = UserSession(base_url=app_url)

    def get_user(self, user_id: int) -> ResponseGetUser:
        resp = self.session.get(f"/users/{user_id}")
        assert resp.status_code == HTTPStatus.OK
        return ResponseGetUser(response=resp)
