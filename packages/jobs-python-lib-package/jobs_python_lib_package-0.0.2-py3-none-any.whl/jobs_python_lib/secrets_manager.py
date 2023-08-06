import json
import os

import boto3

import constants

CONNECTION_POOL = None


def get_job_service_client_secret():
    secrets_client = boto3.client("secretsmanager", region_name='us-east-1')
    secret_name = os.environ[constants.ENV_JOB_SERVICE_CLIENT_SECRET]

    secrets_value_response = secrets_client.get_secret_value(SecretId=secret_name).get('SecretString')
    secret_value = json.loads(secrets_value_response)

    client_secret = secret_value[constants.ENV_JOB_SERVICE_CLIENT_SECRET]

    return client_secret
