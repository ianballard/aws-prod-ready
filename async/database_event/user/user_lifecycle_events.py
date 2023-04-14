from core_lib.services.search import search_service
import os


def handle_user_event(event_name, old_image, new_image):
    handler = EVENT_TYPES.get(event_name)
    return handler(old_image, new_image)


def user_inserted(old_image, new_image):
    print(f"user_inserted: {old_image} {new_image}")

    if is_search_enabled():
        search_service.upsert_user(new_image)


def user_modified(old_image, new_image):
    print(f"user_modified: {old_image} {new_image}")

    if is_search_enabled():
        search_service.upsert_user(new_image)


def user_deleted(old_image, new_image):
    print(f"user_deleted: {old_image} {new_image}")


EVENT_TYPES = {"INSERT": user_inserted, "MODIFY": user_modified, "REMOVE": user_deleted}


def is_search_enabled():
    return os.getenv('SEARCH_ENABLED') == 'true'
