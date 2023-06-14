from unittest.mock import patch, MagicMock

from api.user import user_controller
from api_lib.response.api_response import ApiResponse
from core_lib.utils.json_schema_util import ACTIVE_STATUS


@patch("api.user.user_controller.auth_service")
@patch("api.user.user_controller.database_service")
def test_health(database_service, auth_service):
    auth_service.health_check.return_value = None
    database_service.health_check.return_value = None

    response = user_controller.health(event={}, context=None)
    assert response == ApiResponse(
        request_headers={},
        status_code=200,
        response_body=None,
    ).format(skip_access_log=True)


@patch("api.user.user_controller.safe_get_thread_attribute")
@patch("api.user.user_controller.user_association_data_access")
@patch("api_lib.auth.authorization.get_decoded_jwt")
def test_query(
    mock_get_decoded_jwt, user_association_data_access, safe_get_thread_attribute
):
    mock_get_decoded_jwt.return_value = {"profile": "user-abc"}
    safe_get_thread_attribute.return_value = "user_id"
    expected_query_results = {
        "last_evaluated_key": "next",
        "items": [
            {
                "profile": "abc",
                "username": "abc",
                "first_name": "abc",
                "last_name": "abc",
                "email": "email@email.com",
                "entity_status": ACTIVE_STATUS,
            }
        ],
    }
    user_association_data_access.query_associated_users_with_profiles.return_value = (
        expected_query_results
    )
    headers = {"Authorization": "bearer foo"}

    response = user_controller.query(event={"headers": headers}, context={})
    assert response == ApiResponse(
        request_headers=headers,
        status_code=200,
        response_body=expected_query_results,
    ).format(skip_access_log=True)
