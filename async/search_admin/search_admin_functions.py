from core_lib.services.search import search_service
from core_lib.utils.cloudformation_custom_resource_util import send_cfn_response
from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.thread_util import safe_get_thread_attribute


@lambda_handler()
def assign_read_access(event):
    if (
        event.get("RequestType") == "Create"
        and not search_service.is_domain_processing_changes()
    ):
        search_service.assign_access(
            role_name="readall_and_monitor",
            target_function_role_tag_value="search_read_function",
        )

    send_cfn_response(
        event,
        safe_get_thread_attribute("context"),
        "SUCCESS",
        {"Message": "Lambda function triggered"},
    )


@lambda_handler()
def assign_write_access(event):
    if (
        event.get("RequestType") == "Create"
        and not search_service.is_domain_processing_changes()
    ):
        search_service.assign_access(
            role_name="all_access",
            target_function_role_tag_value="search_write_function",
        )

    send_cfn_response(
        event,
        safe_get_thread_attribute("context"),
        "SUCCESS",
        {"Message": "Lambda function triggered"},
    )


@lambda_handler()
def enable_audit_logs(event):
    if (
        event.get("RequestType") == "Create"
        and not search_service.is_domain_processing_changes()
    ):
        search_service.enable_audit_logs()

    send_cfn_response(
        event,
        safe_get_thread_attribute("context"),
        "SUCCESS",
        {"Message": "Lambda function triggered"},
    )


@lambda_handler()
def create_user_index(event):
    if (
        event.get("RequestType") == "Create"
        and not search_service.is_domain_processing_changes()
        and search_service.user_index_exists() is False
    ):
        search_service.create_user_index()

    send_cfn_response(
        event,
        safe_get_thread_attribute("context"),
        "SUCCESS",
        {"Message": "Lambda function triggered"},
    )
