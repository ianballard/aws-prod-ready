from api_lib.request.api_request import ApiRequest, api
from api_lib.response.api_response import ApiResponse
from core_lib.data_models.user import user_data_access
from core_lib.services.auth import auth_service
from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.uuid_util import generate_uuid


@lambda_handler()
@api()
def signup(api_request: ApiRequest):
    request_body = api_request.body
    username = request_body.get("username")
    email = request_body.get("email")
    password = request_body.get("password")
    first_name = request_body.get("first_name")
    last_name = request_body.get("last_name")
    profile = generate_uuid()
    signup_response = auth_service.sign_up(
        profile=profile,
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    user_data_access.create_user(
        {
            "profile": profile,
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
        }
    )
    return ApiResponse(
        request_headers=api_request.headers,
        status_code=201,
        response_body=signup_response,
    ).format()


@lambda_handler()
@api()
def confirm_sign_up(api_request: ApiRequest):
    query_parameters = api_request.query_parameters
    username = query_parameters.get("username")
    code = query_parameters.get("code")
    auth_service.confirm_sign_up(username=username, code=code)
    return ApiResponse(
        request_headers=api_request.headers, status_code=200, response_body=None
    ).format()


@lambda_handler()
@api()
def authenticate(api_request: ApiRequest):
    request_body = api_request.body
    username = request_body.get("username")
    password = request_body.get("password")
    authentication_response = auth_service.initiate_user_password_auth(
        username=username, password=password
    )
    return ApiResponse(
        request_headers=api_request.headers,
        status_code=200,
        response_body=authentication_response,
    ).format()
