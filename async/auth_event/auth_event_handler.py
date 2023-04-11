import json

from core_lib.services.auth import auth_service
from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.log_util import log_unexpected_exception, log_warning


@lambda_handler()
def handle_auth_event(event):
    for record in event.get("Records", []):
        try:
            message = json.loads(record.get("body"))
            event_type = message.get("event_type")
            handler = EVENT_TYPE_HANDLERS.get(event_type)
            if not handler:
                log_warning(f"missing handler for event: {event_type}")
                continue

            handler(**message.get("args", {}))
        except Exception as e:
            log_unexpected_exception(e)


def handle_sign_up(
    profile: str,
    username: str,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
):
    auth_service.admin_create_user(
        profile=profile,
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        suppress_message=True,
        is_password_permanent=True,
    )
    auth_service.admin_disable_user(username=username)


def handle_confirm_sign_up(username: str, code: str):
    auth_service.confirm_sign_up(username=username, code=code)


EVENT_TYPE_HANDLERS = {
    "replicated_sign_up": handle_sign_up,
    "replicated_confirm_sign_up": handle_confirm_sign_up,
}
