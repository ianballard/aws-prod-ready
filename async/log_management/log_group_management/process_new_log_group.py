import os

from core_lib.services.logs.impl.cloudwatch_logs_service import (
    put_subscription_filter,
    encrypt_log_group,
    put_retention_policy,
    build_log_group_name_from_arn,
)
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

    encrypt_log_group(
        log_group_name=new_log_group_name, kms_key_arn=os.getenv("LOGS_KMS_KEY_ARN")
    )

    retention_in_days = 90
    set_subscription_filters = True
    if is_log_group_central(
        new_log_group_name=new_log_group_name,
        access_log_group_name=access_log_group_name,
        error_log_group_name=error_log_group_name,
    ):
        # 7 year retention as defined by logs service
        retention_in_days = 2557
        # avoid circular dependency
        set_subscription_filters = False

    put_retention_policy(
        log_group_name=new_log_group_name, retention_in_days=retention_in_days
    )

    if set_subscription_filters:
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
    else:
        log_info(
            f"new log group is a log target destination. skipping subscription filter creation. "
            f"new_log_group_name: {new_log_group_name} "
            f"access_log_group_name: {access_log_group_name} "
            f"error_log_group_name: {error_log_group_name}"
        )


def is_log_group_central(
    new_log_group_name: str, access_log_group_name: str, error_log_group_name: str
):
    return (
        new_log_group_name == access_log_group_name
        or new_log_group_name == error_log_group_name
    )
