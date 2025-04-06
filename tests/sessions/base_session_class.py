import logging
import curlify

from requests import Session, Response


class UserSession(Session):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.base_url = kwargs.get('base_url', None)

    def request(self, method, url, **kwargs):
        url: str = self.base_url + url
        response: Response = super().request(method, url, **kwargs)
        logging.info(curlify.to_curl(response.request))
        return response
