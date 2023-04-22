import os

from core_lib.services.logs.impl.cloudwatch_logs_service import put_subscription_filter
from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.log_util import log_warning


@lambda_handler()
def handle_new_log_group_created(event):
    log_group_name = event.get('detail', {}).get('requestParameters', {}).get('logGroupName')

    if not log_group_name:
        log_warning('no log group name provided')
        return

    put_subscription_filter(
        log_group=log_group_name,
        destination_arn=os.getenv("APP_ERROR_LOGGER_FUNCTION_ARN"),
        filter_name="error_log_filter",
        filter_pattern="APP_ERROR_LOG"
    )

    put_subscription_filter(
        log_group=log_group_name,
        destination_arn=os.getenv("APP_ACCESS_LOGGER_FUNCTION_ARN"),
        filter_name="access_log_filter",
        filter_pattern="APP_ACCESS_LOG"
    )
