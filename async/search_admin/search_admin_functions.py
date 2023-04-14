import json

import boto3

from core_lib.utils.lambda_util import lambda_handler
from core_lib.services.search import search_service
import requests
from requests_aws4auth import AWS4Auth


@lambda_handler()
def assign_readall_and_monitor_role(event):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "osd-xsrf": "True",
    }
    mapping = {"backend_roles": ["*"], "hosts": [], "users": ["*"]}
    role_name = "readall_and_monitor"
    url = (
        f"https://{search_service.get_search_domain_url()}"
        f"/_dashboards/api/v1/configuration/rolesmapping/{role_name}"
    )
    session = boto3.Session()
    credentials = session.get_credentials()
    region = session.region_name

    awsauth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region,
        "es",
        session_token=credentials.token,
    )

    response = requests.post(
        url, timeout=3, headers=headers, data=json.dumps(mapping), auth=awsauth
    )
    print(f"response status_code: {response.status_code}")
    print(f"response body: {response.json()}")


@lambda_handler()
def enable_audit_logs(event):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "osd-xsrf": "true",
    }
    config = {
        "compliance": {
            "enabled": True,
            "write_log_diffs": False,
            "read_watched_fields": {},
            "read_ignore_users": [],
            "write_watched_indices": [],
            "write_ignore_users": [],
            "read_metadata_only": True,
            "write_metadata_only": True,
            "external_config": False,
            "internal_config": True,
        },
        "enabled": True,
        "audit": {
            "ignore_users": [],
            "ignore_requests": [],
            "disabled_rest_categories": ["AUTHENTICATED", "GRANTED_PRIVILEGES"],
            "disabled_transport_categories": ["AUTHENTICATED", "GRANTED_PRIVILEGES"],
            "log_request_body": False,
            "resolve_indices": True,
            "resolve_bulk_requests": False,
            "exclude_sensitive_headers": True,
            "enable_transport": False,
            "enable_rest": True,
        },
    }
    url = (
        f"https://{search_service.get_search_domain_url()}"
        f"/_dashboards/api/v1/configuration/audit/config"
    )
    session = boto3.Session()
    credentials = session.get_credentials()
    region = session.region_name

    awsauth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region,
        "es",
        session_token=credentials.token,
    )

    response = requests.post(
        url, timeout=3, headers=headers, data=json.dumps(config), auth=awsauth
    )
    print(f"response status_code: {response.status_code}")
    print(f"response body: {response.json()}")


@lambda_handler()
def create_user_index(event):
    search_service.create_user_index()
