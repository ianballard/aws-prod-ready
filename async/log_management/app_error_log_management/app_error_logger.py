from core_lib.utils.lambda_util import lambda_handler
from core_lib.services.logs import log_service


@lambda_handler()
def log_error_event(event):
    log_service.log_subscribed_log_events(event=event)
