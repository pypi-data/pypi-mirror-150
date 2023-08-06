import base64
import logging
import os
import requests
from jobs_python_lib import constants
from jobs_python_lib.secrets_manager import get_job_service_client_secret
from requests import Timeout

logger = logging.getLogger('jobs_python_lib')
logger.setLevel(logging.INFO)


def validate_authorization(event_context):
    auth_tokens = get_auth_tokens(event_context)
    auth_response = None

    auth_token = auth_tokens[0]

    if auth_token is not None and len(auth_token) > 0:
        auth_response = jwt_authentication(auth_tokens[0])
    elif auth_tokens[1] is not None and len(auth_tokens[1]) > 0:
        auth_response = validate_access_token(auth_tokens[1])

    if auth_response is not None:
        identity_data = get_identity_data(auth_response)  # Not sure if we will even need this for company
        print(identity_data)

    return auth_response


def get_auth_tokens(event_context):
    auth_token = event_context.get('authToken')
    legacy_auth_token = event_context.get('legacyAuthToken')

    return auth_token, legacy_auth_token


def jwt_authentication(jwt):  # pylint: disable=inconsistent-return-statements
    try:
        jwt_url = os.environ[constants.ENV_SECURE_DOMAIN] + constants.JWT_TOKEN_PATH
        data = get_jwt_data(jwt)
        client_id = os.environ[constants.ENV_JOB_SERVICE_CLIENT_ID]
        client_secret = get_job_service_client_secret()
        headers = get_jwt_headers(client_id, client_secret)
        resp = requests.post(jwt_url, data=data, headers=headers)
        if resp.status_code == 200:  # pylint: disable=no-else-return
            return resp.json()
        else:
            raise Exception('Cannot validate jwt access token', resp.json())
    except Timeout:
        logger.error('The request to jwt validation has timed out.')


def get_jwt_data(jwt):
    payload = {
        'grant_type': "federated_login",
        'access_token': jwt
    }
    return payload


def validate_access_token(legacy_access_token):  # pylint: disable=inconsistent-return-statements
    try:
        oauth_url = os.environ[constants.ENV_SECURE_DOMAIN] + constants.VALIDATIONS_PATH + '?' + constants.TOKEN + '=' + legacy_access_token
        resp = requests.get(oauth_url)
        if resp.status_code == 200:
            response_text = resp.json()
            if response_text.get('error') is None:  # pylint: disable=no-else-return
                return response_text
            else:
                raise Exception('Cannot validate legacy access token')
        else:
            raise Exception('Cannot validate legacy access token')
    except Timeout:
        logger.error('The request to oauth token validation has timed out.')


def get_jwt_headers(client_id, client_secret):
    return {
        constants.HEADER_AUTHORIZATION: get_basic_auth_header(client_id, client_secret),
        constants.HEADER_CONTENT_TYPE: constants.CONTENT_TYPE_URLENCODED
    }


def get_basic_auth_header(client_id, client_secret):
    auth_string = client_id + ":" + client_secret
    return "Basic " + str(base64.b64encode(auth_string.encode(constants.CONTENT_ENCODING)), constants.CONTENT_ENCODING)


def get_identity_data(legacy_token_validation_dict):
    company_id = legacy_token_validation_dict.get('company_id')
    user_id = legacy_token_validation_dict.get('user_id')
    user_name = legacy_token_validation_dict.get('username')
    user_type = legacy_token_validation_dict.get('user_type')

    identity_data = {
        'company_id': company_id,
        'user_id': user_id,
        'user_name': user_name,
        'user_type': user_type
    }

    return identity_data
