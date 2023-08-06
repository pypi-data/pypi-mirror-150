from coreutility.collection.dictionary_utility import as_data

from coreauth.exception.AuthenticatorError import AuthenticatorError
from coreauth.exception.UnableToAuthenticateError import UnableToAuthenticateError
from coreauth.repository.AuthRepository import AuthRepository

AUTH_URL = 'AUTH_URL'


class Authenticator:

    def __init__(self, options):
        self.auth_url = options[AUTH_URL]
        self.repository = AuthRepository(options)

    def logon(self):
        pass

    def logoff(self):
        pass

    def refresh(self):
        pass

    def obtain_auth_value(self, value):
        auth_info = self.repository.retrieve()
        if auth_info is None or len(auth_info) == 0:
            raise UnableToAuthenticateError('AUTH_INFO not available')
        auth_value = as_data(auth_info, value)
        if auth_value is None or len(auth_value) == 0:
            raise UnableToAuthenticateError(f'AUTH_INFO does not contain {value}')
        return auth_value

    @staticmethod
    def should_update_url() -> bool:
        return False

    def update_url(self, url) -> str:
        raise AuthenticatorError('Update URL needs to be implemented')
