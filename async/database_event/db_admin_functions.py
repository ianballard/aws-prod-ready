import os

import boto3

from core_lib.services.cloud_function.impl import lambda_service
from core_lib.utils.cloudformation_custom_resource_util import send_cfn_response
from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.thread_util import safe_get_thread_attribute

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
