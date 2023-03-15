from user.user_lifecycle_events import handle_user_event
from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.log_util import log_unexpected_exception, log_warning
from core_lib.services.database.impl.dynamodb_service import dynamodb_json_to_json

@lambda_handler()
def handle_db_event(event):
    records = event.get("Records", [])

    for record in records:
        try:
            db_event = record.get('dynamodb', {})
            event_name = record.get('eventName')
            old_image = dynamodb_json_to_json(db_event.get("OldImage", {}))
            new_image = dynamodb_json_to_json(db_event.get("NewImage", {}))
            entity_type = new_image.get("EntityType") \
                if event_name in ['INSERT', 'MODIFY'] \
                else old_image.get("EntityType")

            if not entity_type:
                log_warning(f'missing EntityType attribute: {new_image}')
                continue
            entity_type_handler = ENTITY_TYPES.get(entity_type)

            if not entity_type_handler:
                log_warning(f'missing entity_type_handler for entity: {entity_type}')
                continue

            entity_response = entity_type_handler(event_name, old_image, new_image)
        except Exception as e:
            log_unexpected_exception(e)


ENTITY_TYPES = {"user": handle_user_event}
