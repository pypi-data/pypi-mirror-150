from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.options.exception.MissingOptionError import MissingOptionError

AUTH_INFO_KEY = 'AUTH_INFO_KEY'


class AuthRepository:

    def __init__(self, options):
        self.options = options
        self.__check_options()
        self.cache = RedisCacheHolder()

    def __check_options(self):
        if self.options is None:
            raise MissingOptionError(f'missing option please provide options {AUTH_INFO_KEY}')
        if AUTH_INFO_KEY not in self.options:
            raise MissingOptionError(f'missing option please provide option {AUTH_INFO_KEY}')

    def store(self, auth_info: dict):
        key = self.options[AUTH_INFO_KEY]
        self.cache.store(key, auth_info)

    def retrieve(self) -> dict:
        key = self.options[AUTH_INFO_KEY]
        return self.cache.fetch(key, as_type=dict)
