import json
from unittest.mock import patch

from api.auth import auth_controller
from api_lib.response.api_response import ApiResponse


@patch("api.auth.auth_controller.auth_service.initiate_user_password_auth")
def test_authenticate(initiate_user_password_auth):

    event = {
        'headers': {},
        'pathParameters': {},
        'body': json.dumps({
            'username': 'foo',
            'password': 'bar'
        }),
        'queryStringParameters': {}
    }

    expected_auth_service_return_value = {
        "ChallengeParameters": {},
        "AuthenticationResult": {
            "AccessToken": "access_token_value",
            "ExpiresIn": 3600,
            "TokenType": "Bearer",
            "RefreshToken": "refresh_token_value",
            "IdToken": "id_token_value"
        }
    }

    initiate_user_password_auth.return_value = expected_auth_service_return_value

    authenticate_response = auth_controller.authenticate(event, None)

    api_response = ApiResponse(request_headers=event['headers'], status_code=200)

    assert authenticate_response == {
        'headers': api_response.headers,
        'statusCode': api_response.status_code,
        'body': json.dumps(expected_auth_service_return_value)
    }

    initiate_user_password_auth.assert_called_once_with(**json.loads(event['body']))
