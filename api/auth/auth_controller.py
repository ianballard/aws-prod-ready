from core_lib.services.auth.auth_service import sign_up, initiate_user_password_auth
from api_lib.auth.authorization import authorize, Authorization, UserGroup
from core_lib.utils.lambda_util import lambda_handler
from api_lib.request.api_request import ApiRequest, api
from api_lib.response.api_response import ApiResponse


@lambda_handler()
@api()
def signup(api_request: ApiRequest):
    request_body = api_request.body
    email = request_body.get("email")
    password = request_body.get("password")
    first_name = request_body.get("first_name")
    last_name = request_body.get("last_name")
    signup_response = sign_up(
        email=email, password=password, first_name=first_name, last_name=last_name
    )
    return ApiResponse(
        request_headers=api_request.headers,
        status_code=201,
        response_body=signup_response,
    ).format()


@lambda_handler()
@api()
def authenticate(api_request: ApiRequest):
    request_body = api_request.body
    username = request_body.get("username")
    password = request_body.get("password")
    authentication_response = initiate_user_password_auth(
        username=username, password=password
    )
    return ApiResponse(
        request_headers=api_request.headers,
        status_code=200,
        response_body=authentication_response,
    ).format()
