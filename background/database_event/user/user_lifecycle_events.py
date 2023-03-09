def handle_user_event(record):
    event_name = record["eventName"]
    handler = EVENT_TYPES.get(event_name)
    return handler(record)


def user_inserted(record):
    print("user_inserted")


def user_modified(record):
    print("user_modified")


def user_deleted(record):
    print("user_deleted")


EVENT_TYPES = {"INSERT": user_inserted, "MODIFY": user_modified, "DELETE": user_deleted}
