from http import HTTPStatus

from tests.config.config import Server
from tests.sessions.base_session_class import UserSession
from tests.models.ResponseGetUser import ResponseGetUser


class UserService:
    def __init__(self, env):
        self.session = UserSession(base_url=Server(env).users_app)

    def get_user(self, user_id: int) -> ResponseGetUser:
        resp = self.session.get(f"/api/users/{user_id}")
        assert resp.status_code == HTTPStatus.OK
        return ResponseGetUser(response=resp)
