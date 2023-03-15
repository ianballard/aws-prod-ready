from core_lib.utils.log_util import log_unexpected_exception
from core_lib.utils.lambda_util import lambda_handler
import json


@lambda_handler()
def log_error_event(event):
    for record in event.get("Records", []):
        try:
            print(json.loads(record.get("body")))
        except Exception as e:
            log_unexpected_exception(e, send_error_to_error_log_queue=False)