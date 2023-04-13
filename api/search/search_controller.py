from api_lib.request.api_request import ApiRequest, api
from api_lib.response.api_response import ApiResponse
from core_lib.services.search import search_service
from core_lib.utils.lambda_util import lambda_handler


@lambda_handler()
@api()
def search(api_request: ApiRequest):
    return ApiResponse(
        request_headers=api_request.headers,
        status_code=201,
        response_body=search_service.get_client_info(),
    ).format()
