from api_lib.auth.authorization import (
    authorize,
    Authorization,
    ResourceAccess,
    ActionType,
)
from api_lib.request.api_request import ApiRequest, api
from api_lib.response.api_response import ApiResponse
from core_lib.data_access.user import user_data_access, user_association_data_access
from core_lib.services.auth import auth_service
from core_lib.services.database import database_service
from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.thread_util import safe_get_thread_attribute


@lambda_handler()
@api()
def health(api_request: ApiRequest):

    auth_service.health_check()

    database_service.health_check()

    return ApiResponse(
        request_headers=api_request.headers,
        status_code=200,
        response_body=None,
    ).format()


@lambda_handler()
@api()
@authorize(
    Authorization(
        action_type=ActionType.List,
        resource_access=ResourceAccess.AccessUser,
    )
)
def query(api_request: ApiRequest):
    return ApiResponse(
        api_request.headers,
        status_code=200,
        response_body=user_association_data_access.query_associated_users_with_profiles(
            user_a_id=safe_get_thread_attribute("principle")
        ),
    ).format()


@lambda_handler()
@api()
@authorize(
    Authorization(
        action_type=ActionType.Get,
        resource_access=ResourceAccess.AccessUser,
    )
)
def get(api_request: ApiRequest):
    path_parameters = api_request.path_parameters
    return ApiResponse(
        api_request.headers,
        status_code=200,
        response_body=user_data_access.find_user_by_id(
            _id=path_parameters.get("id"),
            projection_expression="profile,username,first_name,last_name,email,entity_status",
        ),
    ).format()


@lambda_handler()
@api()
@authorize(
    Authorization(
        action_type=ActionType.Update,
        resource_access=ResourceAccess.AccessUser,
    )
)
def update(api_request: ApiRequest):
    path_parameters = api_request.path_parameters
    updates = api_request.body
    user_data_access.update_user(_id=path_parameters.get("id"), updates=updates)
    return ApiResponse(
        api_request.headers,
        status_code=200,
        response_body=updates,
    ).format()


@lambda_handler()
@api()
@authorize(
    Authorization(
        action_type=ActionType.Delete,
        resource_access=ResourceAccess.AccessUser,
    )
)
def delete(api_request: ApiRequest):
    path_parameters = api_request.path_parameters
    user_data_access.delete_user_by_id(path_parameters.get("id"))
    return ApiResponse(
        api_request.headers,
        status_code=204,
        response_body=None,
    ).format()


@lambda_handler()
@api()
@authorize(
    Authorization(
        action_type=ActionType.Associate,
        resource_access=ResourceAccess.AccessUser,
    )
)
def associate(api_request: ApiRequest):
    path_parameters = api_request.path_parameters
    return ApiResponse(
        api_request.headers,
        status_code=201,
        response_body=user_association_data_access.associate_users(
            user_a_id=safe_get_thread_attribute("principle"),
            user_b_id=path_parameters.get("id"),
        ),
    ).format()
