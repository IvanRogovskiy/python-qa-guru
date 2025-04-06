from requests import Response


class ResponseGetUser:

    def __init__(self, **kwargs):
        response: Response = kwargs.pop("response", None)
        self.response_ = response
        json = response.json()
        self.json_ = {
            "name": json["name"],
            "email": json["email"],
            "id": json["id"]
        }

    @property
    def name(self) -> str:
        return self.json_["name"]

    @property
    def email(self) -> str:
        return self.json_["email"]

    @property
    def id(self) -> str:
        return self.json_["id"]

    @property
    def response(self):
        return self.response_

    @property
    def json(self) -> dict:
        return self.json_
