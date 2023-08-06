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
