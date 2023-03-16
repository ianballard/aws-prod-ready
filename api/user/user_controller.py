from api_lib.auth.authorization import authorize, Authorization, UserGroup
from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.thread_util import safe_get_thread_attribute
from api_lib.request.api_request import ApiRequest, api
from api_lib.response.api_response import ApiResponse
from core_lib.services.database.database_service import (
    get_item,
    put_item,
    query_items,
    delete_item,
    update_item,
)


@lambda_handler()
@api()
@authorize(Authorization(user_group=UserGroup.User))
def put(api_request: ApiRequest):
    item = api_request.body
    return ApiResponse(
        api_request.headers, status_code=200, response_body=put_item(Item=item)
    ).format()


@lambda_handler()
@api()
@authorize(Authorization(user_group=UserGroup.User))
def query(api_request: ApiRequest):
    query_parameters = api_request.query_parameters
    key = {"pk": query_parameters.get("pk"), "sk": query_parameters.get("sk")}
    return ApiResponse(
        api_request.headers, status_code=200, response_body=query_items(Item=key)
    ).format()


@lambda_handler()
@api()
@authorize(Authorization(user_group=UserGroup.User))
def get(api_request: ApiRequest):
    path_parameters = api_request.path_parameters
    key = {"pk": "user", "sk": path_parameters.get("id")}
    return ApiResponse(
        api_request.headers, status_code=200, response_body=get_item(Key=key)
    ).format()


@lambda_handler()
@api()
@authorize(Authorization(user_group=UserGroup.User))
def update(api_request: ApiRequest):
    path_parameters = api_request.path_parameters
    key = {"pk": "user", "sk": path_parameters.get("id")}
    update_expression = "set a=:v0, b=:v1"
    expression_attribute_values = {":v0": "test1", ":v1": "test2"}
    return ApiResponse(
        api_request.headers,
        status_code=200,
        response_body=update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW",
        ),
    ).format()


@lambda_handler()
@api()
@authorize(Authorization(user_group=UserGroup.User))
def delete(api_request: ApiRequest):
    path_parameters = api_request.path_parameters
    key = {"pk": "user", "sk": path_parameters.get("id")}

    return ApiResponse(
        api_request.headers, status_code=200, response_body=delete_item(Key=key)
    ).format()
