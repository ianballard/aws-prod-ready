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
    if (
        new_log_group_name
        == f"/aws/lambda/{get_lambda_function_name(error_log_destination_arn)}"
    ):
        log_info(
            "new log group is the error log target destination. skipping subscription filter creation."
        )
        return

    log_info(f"creating error log subscription filter for {new_log_group_name}.")
    # TODO check to see if the log group lambda belongs to the same stack or move central logging lambdas to long lived resources
    # put_subscription_filter(
    #     log_group=new_log_group_name,
    #     destination_arn=error_log_destination_arn,
    #     filter_name="error_log_filter",
    #     filter_pattern="APP_ERROR_LOG",
    # )

    access_log_destination_arn = os.getenv("APP_ACCESS_LOGGER_FUNCTION_ARN")
    if (
        f"/aws/lambda/{get_lambda_function_name(access_log_destination_arn)}"
        != new_log_group_name
    ):
        log_info(f"creating access log subscription filter for {new_log_group_name}.")
        # put_subscription_filter(
        #     log_group=new_log_group_name,
        #     destination_arn=access_log_destination_arn,
        #     filter_name="access_log_filter",
        #     filter_pattern="APP_ACCESS_LOG",
        # )
    else:
        log_info(
            "new log group is the access log target destination. skipping subscription filter creation."
        )


def get_lambda_function_name(arn):
    return arn.split(":")[-1]
