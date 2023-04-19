from api_lib.auth.authorization import authorize, Authorization, ActionType, ResourceAccess
from api_lib.request.api_request import ApiRequest, api
from api_lib.response.api_response import ApiResponse
from core_lib.services.search import search_service
from core_lib.utils.lambda_util import lambda_handler


@lambda_handler()
@api()
@authorize(
    Authorization(
        action_type=ActionType.List,
        resource_access=ResourceAccess.AccessSearch,
    )
)
def search_users(api_request: ApiRequest):
    search_str = api_request.body.get("search_str")

    return ApiResponse(
        request_headers=api_request.headers,
        status_code=200,
        response_body=search_service.search_users(search_str=search_str),
    ).format()
