from api_lib.auth.authorization import (
    authorize,
    Authorization,
    UserGroup,
    ResourceAccess,
    ActionType,
)
from api_lib.request.api_request import ApiRequest, api
from api_lib.response.api_response import ApiResponse
from core_lib.data_models.user import user_data_access
from core_lib.utils.lambda_util import lambda_handler


@lambda_handler()
@api()
@authorize(
    Authorization(
        user_group=UserGroup.Admin,
        action_type=ActionType.Create,
        resource_access=ResourceAccess.AccessUser,
    )
)
def put(api_request: ApiRequest):
    item = api_request.body
    return ApiResponse(
        api_request.headers,
        status_code=200,
        response_body=user_data_access.create_user(item),
    ).format()


@lambda_handler()
@api()
@authorize(
    Authorization(
        user_group=UserGroup.User,
        action_type=ActionType.List,
        resource_access=ResourceAccess.AccessUser,
    )
)
def query(api_request: ApiRequest):
    return ApiResponse(
        api_request.headers,
        status_code=200,
        response_body=user_data_access.query_all_users(),
    ).format()


@lambda_handler()
@api()
@authorize(
    Authorization(
        user_group=UserGroup.User,
        action_type=ActionType.Get,
        resource_access=ResourceAccess.AccessUser,
    )
)
def get(api_request: ApiRequest):
    path_parameters = api_request.path_parameters
    return ApiResponse(
        api_request.headers,
        status_code=200,
        response_body=user_data_access.find_user_by_id(_id=path_parameters.get("id")),
    ).format()


@lambda_handler()
@api()
@authorize(
    Authorization(
        user_group=UserGroup.User,
        action_type=ActionType.Update,
        resource_access=ResourceAccess.AccessUser,
    )
)
def update(api_request: ApiRequest):
    path_parameters = api_request.path_parameters
    updates = api_request.body
    return ApiResponse(
        api_request.headers,
        status_code=200,
        response_body=user_data_access.update_user(
            _id=path_parameters.get("id"), updates=updates
        ),
    ).format()


@lambda_handler()
@api()
@authorize(
    Authorization(
        user_group=UserGroup.Admin,
        action_type=ActionType.Delete,
        resource_access=ResourceAccess.AccessUser,
    )
)
def delete(api_request: ApiRequest):
    path_parameters = api_request.path_parameters
    return ApiResponse(
        api_request.headers,
        status_code=200,
        response_body=user_data_access.delete_user_by_id(path_parameters.get("id")),
    ).format()
