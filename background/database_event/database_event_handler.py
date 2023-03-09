from background.database_event.user.user_lifecycle_events import handle_user_event


def handle_db_event(event, context):
    records = event.get("Records", [])

    for record in records:
        new_image = record.get("NewImage", {})
        entity_type = new_image.get("EntityType")
        entity_type_handler = ENTITY_TYPES.get(entity_type)
        entity_response = entity_type_handler(record)


ENTITY_TYPES = {"user": handle_user_event}
