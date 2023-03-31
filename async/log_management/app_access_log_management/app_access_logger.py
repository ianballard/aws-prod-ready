from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.log_util import log_subscribed_log_events


@lambda_handler()
def log_access_event(event):
    log_subscribed_log_events(event)
