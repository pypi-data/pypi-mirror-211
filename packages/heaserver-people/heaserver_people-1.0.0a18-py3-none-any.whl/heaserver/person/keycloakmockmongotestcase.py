import configparser
import logging
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Generator

from aiohttp.web_request import Request
from heaobject.person import Person
from heaobject.root import ShareImpl, Permission
from heaobject.user import NONE_USER, ALL_USERS
from heaserver.service.testcase.mockmongo import MockMongo, MockMongoManager

from heaserver.person.keycloakmongo import DEFAULT_CLIENT_ID, DEFAULT_REALM, DEFAULT_HOST, DEFAULT_SECRET_FILE, \
    CONFIG_SECTION, _has_permission
from heaserver.person.testcasedata import person1, person2


class KeycloakMockMongo(MockMongo):
    def __init__(self, config: configparser.ConfigParser | None = None,
                 access_token: str | None = None,
                 client_id: str | None = DEFAULT_CLIENT_ID,
                 realm: str | None = DEFAULT_REALM,
                 host: str | None = DEFAULT_HOST,
                 secret: str | None = None,
                 secret_file: str | None = DEFAULT_SECRET_FILE,
                 verify_ssl: bool = False):
        super().__init__(config)
        if config and CONFIG_SECTION in config:
            _section = config[CONFIG_SECTION]
            self.__realm = _section.get('Realm', realm)
            self.__verify_ssl = _section.getboolean('VerifySSL', verify_ssl)
            self.__host = _section.get('Host', host)
            self.__secret = _section.get('Secret', secret)
            self.__secret_file = _section.get('SecretFile', secret_file)
        else:
            self.__realm = realm
            self.__verify_ssl = verify_ssl
            self.__host = host
            self.__secret = secret
            self.__secret_file = secret_file

        self.__access_token = access_token
        self.__client_id = client_id

    @property
    def access_token(self) -> str | None:
        return self.__access_token

    @property
    def client_id(self) -> str:
        return self.__client_id

    @property
    def realm(self) -> str:
        return self.__realm

    @property
    def host(self) -> str:
        return self.__host

    @property
    def secret(self) -> str | None:
        return self.__secret

    @property
    def secret_file(self) -> str | None:
        return self.__secret_file

    @property
    def verify_ssl(self) -> bool:
        return self.__verify_ssl

    async def get_keycloak_access_token(self, request: Request) -> str:
        return '12345678'

    async def get_users(self, request: Request, access_token: str, params: dict[str, str] | None = None) -> list[
        Person]:
        logger = logging.getLogger(__name__)

        persons = []
        for r in (person1, person2):
            if params is None or all(hasattr(r, k) and v == getattr(r, k) for k, v in params.items()):
                persons.append(r)
        return persons

    async def get_user(self, request: Request, access_token: str, id_: str) -> Person | None:
        """
        Gets the user from Keycloak with the given id using the '/auth/admin/realms/{realm}/users/{id}' REST API call.

        :param access_token: the access token to use (required).
        :param session: the client session (required).
        :param id_: the user id (required).
        :return: a Person object.
        :raises ClientResponseError if an error occurred or the person was not found.
        """
        logger = logging.getLogger(__name__)
        match (request.match_info['id']):
            case '666f6f2d6261722d71757578':
                return person1 if _has_permission(request, person1) else None
            case '0123456789ab0123456789ab':
                return person2 if _has_permission(request, person2) else None
            case _:
                return None

    def __keycloak_user_to_person(self, user: dict[str, Any]) -> Person:
        """
        Converts a user JSON object from Keycloak to a HEA Person object.

        :param user: a Keycloak user object as a JSON dict.
        :return: a Person object.
        """
        person = Person()
        person.id = user['id']
        person.name = user['username']
        person.first_name = user.get('firstName')
        person.last_name = user.get('lastName')
        person.email = user.get('email')
        person.created = datetime(2022, 1, 1)
        person.owner = NONE_USER
        share = ShareImpl()
        share.user = ALL_USERS
        share.permissions = [Permission.VIEWER]
        person.shares = [share]
        return person


class KeycloakMockMongoManager(MockMongoManager):
    @contextmanager
    def database(self, config: configparser.ConfigParser = None) -> Generator[MockMongo, None, None]:
        yield KeycloakMockMongo(config)
