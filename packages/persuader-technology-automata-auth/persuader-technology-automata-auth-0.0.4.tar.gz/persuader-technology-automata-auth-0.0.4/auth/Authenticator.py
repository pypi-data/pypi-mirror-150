import hashlib
import hmac
import time

from utility.json_utility import as_data

from auth.exception.UnableToAuthenticateError import UnableToAuthenticateError
from auth.repository.AuthRepository import AuthRepository

AUTH_URL = 'AUTH_URL'


class Authenticator:

    def __init__(self, options):
        self.auth_url = options[AUTH_URL]
        self.repository = AuthRepository(options)

    def should_update_url(self) -> bool:
        return False

    def update_url(self, url) -> str:
        pass

    def authenticate(self):
        pass

    def obtain_auth_value(self, value):
        auth_info = self.repository.retrieve()
        if auth_info is None or len(auth_info) == 0:
            raise UnableToAuthenticateError('AUTH_INFO not available')
        auth_value = as_data(auth_info, value)
        if auth_value is None or len(auth_value) == 0:
            raise UnableToAuthenticateError(f'AUTH_INFO does not contain {value}')
        return auth_value

    def get_timestamp(self):
        return int(time.time() * 1000)

    def sign_secret_value(self, secret, value):
        return hmac.new(secret.encode(), value.encode(), hashlib.sha256).hexdigest()
