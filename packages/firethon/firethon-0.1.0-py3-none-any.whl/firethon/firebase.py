import json

from google.auth.transport import Response
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

from .config import FirebaseConfig


class Firebase:
    scopes = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/firebase.database"
    ]

    def __init__(self, config: FirebaseConfig):
        self.url = config.url
        self.credentials = service_account.Credentials.from_service_account_file(
            config.path_to_service_account_file,
            scopes=self.scopes
        )

    def get_session(self) -> AuthorizedSession:
        return AuthorizedSession(self.credentials)

    def dispatch(self, method, *args, **kwargs):
        with self.get_session() as session:
            response = session.__getattribute__(method)(*args, **kwargs)
        return response

    def get(self, endpoint: str) -> Response:
        response = self.dispatch('get', self.make_endpoint(endpoint))
        return response

    def post(self, endpoint: str, data: dict) -> Response:
        json_data = json.dumps(data)
        response = self.dispatch('post', self.make_endpoint(endpoint), json_data)
        return response

    def put(self, endpoint: str, data: dict) -> Response:
        json_data = json.dumps(data)
        response = self.dispatch('put', self.make_endpoint(endpoint), json_data)
        return response

    def make_endpoint(self, endpoint) -> str:
        return self.url + endpoint
