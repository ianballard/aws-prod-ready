import json
from unittest.mock import patch

from api.auth import auth_controller
from api_lib.response.api_response import ApiResponse


@patch("api.auth.auth_controller.user_data_access.create_user")
@patch("api.auth.auth_controller.auth_service.replicated_sign_up")
@patch("api.auth.auth_controller.generate_uuid")
def test_signup(generate_uuid, replicated_sign_up, create_user):
    username = "User01"

    event = {
        "headers": {},
        "pathParameters": {},
        "body": json.dumps(
            {
                "username": username,
                "password": "Password@123",
                "email": "test-email@gmail.com",
                "first_name": "first",
                "last_name": "last",
            }
        ),
        "queryStringParameters": {},
    }

    generate_uuid.return_value = "uuid_value"

    expected_signup_return_value = {
        "username": username,
        "profile": generate_uuid.return_value,
    }
    replicated_sign_up.return_value = expected_signup_return_value
    create_user.return_value = {}

    sign_up_response = auth_controller.signup(event, None)

    api_response = ApiResponse(request_headers=event["headers"], status_code=201)

    assert sign_up_response == {
        "headers": api_response.headers,
        "statusCode": api_response.status_code,
        "body": json.dumps(expected_signup_return_value),
    }

    sign_up_input = {**json.loads(event["body"]), "profile": generate_uuid.return_value}
    replicated_sign_up.assert_called_once_with(**sign_up_input)

    create_user_input = {**sign_up_input}
    create_user_input.pop("password")
    create_user.assert_called_once_with(create_user_input)


@patch("api.auth.auth_controller.auth_service.replicated_confirm_sign_up")
def test_confirm_signup(replicated_confirm_sign_up):
    event = {
        "headers": {},
        "pathParameters": {},
        "queryStringParameters": {"username": "User01", "code": "123456"},
    }

    replicated_confirm_sign_up.return_value = {}

    sign_up_response = auth_controller.confirm_sign_up(event, None)

    api_response = ApiResponse(request_headers=event["headers"], status_code=200)

    assert sign_up_response == {
        "headers": api_response.headers,
        "statusCode": api_response.status_code,
        "body": None,
    }

    replicated_confirm_sign_up.assert_called_once_with(**event["queryStringParameters"])


@patch("api.auth.auth_controller.auth_service.initiate_user_password_auth")
def test_authenticate(initiate_user_password_auth):
    event = {
        "headers": {},
        "pathParameters": {},
        "body": json.dumps({"username": "User01", "password": "Password@123"}),
        "queryStringParameters": {},
    }

    expected_auth_service_return_value = {
        "ChallengeParameters": {},
        "AuthenticationResult": {
            "AccessToken": "access_token_value",
            "ExpiresIn": 3600,
            "TokenType": "Bearer",
            "RefreshToken": "refresh_token_value",
            "IdToken": "id_token_value",
        },
    }

    initiate_user_password_auth.return_value = expected_auth_service_return_value

    authenticate_response = auth_controller.authenticate(event, None)

    api_response = ApiResponse(request_headers=event["headers"], status_code=200)

    assert authenticate_response == {
        "headers": api_response.headers,
        "statusCode": api_response.status_code,
        "body": json.dumps(expected_auth_service_return_value),
    }

    initiate_user_password_auth.assert_called_once_with(**json.loads(event["body"]))
