from api_lib.auth.authorization import authorize, Authorization, UserGroup, get_principle
from core_lib.utils.lambda_util import lambda_handler
from api_lib.request.api_request import ApiRequest, api
from api_lib.response.api_response import ApiResponse

@lambda_handler()
@api()
@authorize(Authorization(user_group=UserGroup.User))
def get(api_request: ApiRequest):

    print(get_principle())

    return ApiResponse(api_request.headers, status_code=200, response_body={"foo": "bar"}).format()