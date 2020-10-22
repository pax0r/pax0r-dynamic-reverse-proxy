class StaticAuth:
    def __init__(self, auth_token: str):
        self._token = auth_token

    def is_authorized(self, request) -> bool:
        token: str = request.headers.get('Authorization')
        token = token.replace("Bearer ", "")
        return token == self._token
