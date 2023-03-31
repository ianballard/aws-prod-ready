import os

from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.log_util import put_subscription_filters_on_all_lambda_logs


@lambda_handler()
def update_managed_log_groups(event):
    filter_name = "access_log_filter"
    app_access_logger_function_arn = os.getenv("APP_ACCESS_LOGGER_FUNCTION_ARN")
    event_filter = 'APP_ACCESS_LOG'

    put_subscription_filters_on_all_lambda_logs(
        filter_name=filter_name, destination_arn=app_access_logger_function_arn, event_filter=event_filter
    )


def test(e, c):
    import boto3
    logs_client = boto3.client("logs")

    response = logs_client.describe_log_groups(
        logGroupNamePrefix='/aws/lambda',
    )
    for log in response.get('logGroups', []):
        try:
            logs_client.delete_subscription_filter(
                logGroupName=log.get('logGroupName'),
                filterName='error_log_filter',
            )
        except Exception:
            pass