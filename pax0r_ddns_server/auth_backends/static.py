from pax0r_ddns_server.auth_backends.base import AuthBase


class StaticAuth(AuthBase):
    def __init__(self, auth_token: str):
        self._token = auth_token

    def is_authorized(self, request, **kwargs) -> bool:
        token: str = request.headers.get("Authorization", "")
        if "Bearer" in token:
            token = token.replace("Bearer ", "")
            return token == self._token
        return False
