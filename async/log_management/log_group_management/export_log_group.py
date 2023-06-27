import os
from datetime import datetime

from core_lib.services.logs.impl.cloudwatch_logs_service import (
    create_export_task,
    build_log_group_name_from_arn,
)
from core_lib.utils.lambda_util import lambda_handler


@lambda_handler()
def create_export(event):
    log_group_name = build_log_group_name_from_arn(event["function_log_group_arn"])
    days_to_include = event["days_to_include"]

    create_export_task(
        log_group_name=log_group_name,
        destination_bucket=os.getenv("LOG_BACKUP_BUCKET"),
        end_date_time=datetime.utcnow(),
        days_to_include=days_to_include,
    )
