import json
from unittest.mock import patch

from api.search import search_controller
from api_lib.response.api_response import ApiResponse


@patch("api.search.search_controller.auth_service")
@patch("api.search.search_controller.search_service")
def test_health(search_service, auth_service):
    auth_service.health_check.return_value = None
    search_service.health_check.return_value = None

    response = search_controller.health(event={}, context=None)
    assert response == ApiResponse(
        request_headers={},
        status_code=200,
        response_body=None,
    ).format(skip_access_log=True)


@patch("api.search.search_controller.search_service")
@patch("api_lib.auth.authorization.get_decoded_jwt")
def test_search_users(mock_get_decoded_jwt, search_service):
    mock_get_decoded_jwt.return_value = {"profile": "user-abc"}
    expected_search_results = [
        {
            "profile": "test",
            "username": "test",
        }
    ]
    search_service.search_users.return_value = expected_search_results
    headers = {"Authorization": "bearer foo"}

    response = search_controller.search_users(
        event={"headers": headers, "body": json.dumps({"search_str": "test"})},
        context={},
    )
    assert response == ApiResponse(
        request_headers=headers,
        status_code=200,
        response_body=expected_search_results,
    ).format(skip_access_log=True)
