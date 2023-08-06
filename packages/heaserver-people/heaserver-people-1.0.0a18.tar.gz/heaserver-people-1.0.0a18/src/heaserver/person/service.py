"""
The HEA Person Microservice is a wrapper around a Keycloak server for HEA to access user information. It accesses
Keycloak using an admin account. The default account is 'admin' with password of 'admin'. To configure this (and you
must do this to be secure!), add a Keycloak section to the service's configuration file with the following properties:
    Realm = the Keyclock realm from which to request user information.
    VerifySSL = whether to verify the Keycloak server's SSL certificate (defaults to True).
    Host = The Keycloak host (defaults to https://localhost:8444).
    Username = the admin account username (defaults to admin).
    Password = the admin account password.
    PasswordFile = the path to the filename with the password (overrides use of the PASSWORD property).

This microservice tries getting the password from the following places, in order:
    1) the KEYCLOAK_QUERY_USERS_PASSWORD property in the HEA Server Registry Microservice.
    2) the above config file.

If not present in any of those sources, a password of admin will be used.
"""
import logging

from heaserver.service import response
from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.wstl import action, builder_factory
from heaserver.person.keycloakmongo import KeycloakMongoManager
from heaserver.service import appproperty
from aiohttp import ClientResponseError


MONGODB_PERSON_COLLECTION = 'people'

@routes.get('/ping')
async def ping(request: web.Request) -> web.Response:
    """
    For testing whether the service is up.

    :param request: the HTTP request.
    :return: Always returns status code 200.
    """
    return response.status_ok(None)


@routes.get('/people/{id}')
@action(name='heaserver-people-person-get-properties', rel='hea-properties')
@action(name='heaserver-people-person-get-self', rel='self', path='/people/{id}')
async def get_person(request: web.Request) -> web.Response:
    """
    Gets the person with the specified id.
    :param request: the HTTP request.
    :return: the requested person or Not Found.
    ---
    summary: A specific person.
    tags:
        - heaserver-people-get-person
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    logger = logging.getLogger(__name__)
    session = request.app[appproperty.HEA_CLIENT_SESSION]
    access_token = await _get_access_token(request)
    try:
        person = await request.app[appproperty.HEA_DB].get_user(request, access_token, request.match_info['id'])
    except ClientResponseError as e:
        if e.status == 404:
            person = None
        else:
            return response.status_internal_error()
    return await response.get(request, person.to_dict() if person else None)


@routes.get('/people/byname/{name}')
@action(name='heaserver-people-person-get-self', rel='self', path='/people/{id}')
async def get_person_by_name(request: web.Request) -> web.Response:
    """
    Gets the person with the specified id.
    :param request: the HTTP request.
    :return: the requested person or Not Found.
    ---
    summary: A specific person, by name.
    tags:
        - heaserver-people-get-person-by-name
    parameters:
        - $ref: '#/components/parameters/name'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    logger = logging.getLogger(__name__)
    access_token = await _get_access_token(request)
    try:
        persons = await request.app[appproperty.HEA_DB].get_users(request, access_token, params={'name': request.match_info['name']})
        return await response.get(request, persons[0].to_dict() if persons else None)
    except ClientResponseError as e:
        return response.status_generic(e.status, body=e.message)


@routes.get('/people')
@routes.get('/people/')
@action(name='heaserver-people-person-get-properties', rel='hea-properties')
@action(name='heaserver-people-person-get-self', rel='self', path='/people/{id}')
async def get_all_persons(request: web.Request) -> web.Response:
    """
    Gets all persons.
    :param request: the HTTP request.
    :return: all persons.
    ---
    summary: All persons.
    tags:
        - heaserver-people-get-all-persons
    responses:
      '200':
        $ref: '#/components/responses/200'
    """
    logger = logging.getLogger(__name__)
    session = request.app[appproperty.HEA_CLIENT_SESSION]
    logger.debug('headers: %s', request.headers)
    access_token = await _get_access_token(request)
    try:
        persons = await request.app[appproperty.HEA_DB].get_users(request, access_token)
        return await response.get_all(request, [person.to_dict() for person in persons])
    except ClientResponseError as e:
        return response.status_generic(e.status, body=e.message)


def main() -> None:
    config = init_cmd_line(description='Read-only wrapper around Keycloak for accessing user information.',
                           default_port=8080)
    start(db=KeycloakMongoManager, config=config, wstl_builder_factory=builder_factory(__package__))


async def _get_access_token(request: web.Request) -> str:
    return await request.app[appproperty.HEA_DB].get_keycloak_access_token(request)

