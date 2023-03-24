import json

from core_lib.services.auth.impl import cognito_service
from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.log_util import log_unexpected_exception, log_warning


@lambda_handler()
def handle_auth_event(event):
    for record in event.get("Records", []):
        try:
            message = json.loads(record.get("body"))
            event_type = message.get('event_type')
            handler = EVENT_TYPE_HANDLERS.get(event_type)
            if not handler:
                log_warning(f"missing handler for event: {event_type}")
                continue

            response = handler(**message.get('args', {}))
        except Exception as e:
            log_unexpected_exception(e)


def handle_sign_up(username: str, email: str, password: str, first_name: str, last_name: str):
    return cognito_service.sign_up(username=username, email=email, password=password, first_name=first_name, last_name=last_name)


def handle_disable():
    pass


def handle_enable():
    pass


def handle_change_password():
    pass


def handle_verify():
    pass


EVENT_TYPE_HANDLERS = {
    "sign_up": handle_sign_up,
    "disable": handle_disable,
    "enable": handle_enable,
    "change_password": handle_change_password,
    "verify": handle_verify
}
