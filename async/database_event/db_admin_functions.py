import json
import os

import boto3

from core_lib.services.cloud_function.impl import lambda_service
from core_lib.services.database import database_service
from core_lib.services.database.impl.dynamodb_service import dynamodb_json_to_json
from core_lib.services.parameter.parameter_service import (
    get_parameter_value,
    ParameterName,
)
from core_lib.utils.cloudformation_custom_resource_util import send_cfn_response
from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.log_util import log_unexpected_exception, log_warning, log_info
from core_lib.utils.thread_util import safe_get_thread_attribute
from user.user_lifecycle_events import handle_user_event

firehose = boto3.client("firehose")


@lambda_handler()
def create_trigger(event):
    if event.get("RequestType") in ["Create", "Update"]:
        lambda_service.create_database_event_lambda_trigger(
            function_arn=os.getenv("DBStreamHandlerFunctionArn")
        )

    send_cfn_response(
        event,
        safe_get_thread_attribute("context"),
        "SUCCESS",
        {"Message": "Lambda function triggered"},
    )
