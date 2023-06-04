import os

from core_lib.services.logs.impl.cloudwatch_logs_service import put_subscription_filter
from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.log_util import log_warning, log_info


@lambda_handler()
def handle_new_log_group_created(event):
    new_log_group_name = (
        event.get("detail", {}).get("requestParameters", {}).get("logGroupName")
    )

    if not new_log_group_name:
        log_warning("no log group name provided")
        return

    error_log_destination_arn = os.getenv("APP_ERROR_LOGGER_FUNCTION_ARN")
    access_log_destination_arn = os.getenv("APP_ACCESS_LOGGER_FUNCTION_ARN")
    error_log_group_name = build_log_group_name_from_arn(error_log_destination_arn)
    access_log_group_name = build_log_group_name_from_arn(access_log_destination_arn)

    if should_ignore_log_group(
        new_log_group_name=new_log_group_name,
        access_log_group_name=access_log_group_name,
        error_log_group_name=error_log_group_name,
    ):
        log_info(
            f"new log group is a log target destination. skipping subscription filter creation. "
            f"new_log_group_name: {new_log_group_name} "
            f"access_log_group_name: {access_log_group_name} "
            f"error_log_group_name: {error_log_group_name}"
        )
        return

    put_subscription_filter(
        log_group=new_log_group_name,
        destination_arn=error_log_destination_arn,
        filter_name="error_log_filter",
        filter_pattern="APP_ERROR_LOG",
    )

    put_subscription_filter(
        log_group=new_log_group_name,
        destination_arn=access_log_destination_arn,
        filter_name="access_log_filter",
        filter_pattern="APP_ACCESS_LOG",
    )


def get_lambda_function_name(arn):
    return arn.split(":")[-1]


def should_ignore_log_group(
    new_log_group_name: str, access_log_group_name: str, error_log_group_name: str
):
    return (
        new_log_group_name == access_log_group_name
        or new_log_group_name == error_log_group_name
    )


def build_log_group_name_from_arn(arn: str):
    return f"/aws/lambda/{get_lambda_function_name(arn)}"
