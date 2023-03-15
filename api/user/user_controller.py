from api_lib.auth.authorization import authorize, Authorization, UserGroup
from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.thread_util import safe_get_thread_attribute
from api_lib.request.api_request import ApiRequest, api
from api_lib.response.api_response import ApiResponse

@lambda_handler()
@api()
@authorize(Authorization(user_group=UserGroup.User))
def get(api_request: ApiRequest):

    print(safe_get_thread_attribute('principle'))

    return ApiResponse(api_request.headers, status_code=200, response_body={"foo": "bar"}).format()