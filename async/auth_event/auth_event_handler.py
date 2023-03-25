import json

from core_lib.services.auth.impl import cognito_service
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

            response = handler(**message.get("args", {}))
        except Exception as e:
            log_unexpected_exception(e)


def handle_sign_up(
    username: str, email: str, password: str, first_name: str, last_name: str
):
    cognito_service.admin_create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        suppress_message=True,
        is_password_permanent=True,
    )
    cognito_service.admin_disable_user(username=username)


def handle_confirm_sign_up(username: str, code: str):
    cognito_service.confirm_sign_up(username=username, code=code)
    cognito_service.admin_enable_user(username=username)


def handle_respond_to_new_password_auth_challenge(
    username: str, password: str, session: str
):
    cognito_service.admin_set_user_password(username=username, password=password)
    cognito_service.admin_enable_user(username=username)


def handle_admin_create_user(
    username: str,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    suppress_message: bool = False,
    is_password_permanent: bool = False,
):
    cognito_service.admin_create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        suppress_message=True,
        is_password_permanent=False,
    )
    cognito_service.admin_disable_user(username=username)


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
    "confirm_sign_up": handle_confirm_sign_up,
    "respond_to_new_password_auth_challenge": handle_respond_to_new_password_auth_challenge,
    "admin_create_user": handle_admin_create_user,
    "disable": handle_disable,
    "enable": handle_enable,
    "change_password": handle_change_password,
    "verify": handle_verify,
}
