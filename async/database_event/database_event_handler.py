import json

import boto3

from core_lib.services.database.impl.dynamodb_service import dynamodb_json_to_json
from core_lib.services.parameter.parameter_service import (
    get_parameter_value,
    ParameterName,
)
from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.log_util import log_unexpected_exception, log_warning, log_info
from user.user_lifecycle_events import handle_user_event

firehose = boto3.client("firehose")
FIREHOSE_DELIVERY_STREAM = None


def get_firehose_delivery_stream():
    global FIREHOSE_DELIVERY_STREAM

    if FIREHOSE_DELIVERY_STREAM is None:
        FIREHOSE_DELIVERY_STREAM = get_parameter_value(
            parameter_name=ParameterName.FIREHOSE_DELIVERY_STREAM
        )

    return FIREHOSE_DELIVERY_STREAM


@lambda_handler()
def handle_db_event(event):
    records = event.get("Records", [])

    for record in records:
        try:
            db_event = record.get("dynamodb", {})
            event_name = record.get("eventName")
            old_image = dynamodb_json_to_json(db_event.get("OldImage", {}))
            new_image = dynamodb_json_to_json(db_event.get("NewImage", {}))
            entity_type = (
                new_image.get("entity_type")
                if event_name in ["INSERT", "MODIFY"]
                else old_image.get("entity_type")
            )

            if not entity_type:
                log_warning(f"missing EntityType attribute: {new_image}")
                continue
            entity_type_handler = ENTITY_TYPES.get(entity_type)

            if not entity_type_handler:
                log_warning(f"missing entity_type_handler for entity: {entity_type}")
                continue

            entity_type_handler(event_name, old_image, new_image)

            put_firehose_record(event_name, old_image, new_image)

        except Exception as e:
            log_unexpected_exception(e)


ENTITY_TYPES = {"user": handle_user_event}


def put_firehose_record(event_name, old_image, new_image):
    record = new_image if event_name in ["INSERT", "MODIFY"] else old_image

    if event_name == "REMOVE":
        record["is_hard_deleted"] = True

    delivery_stream_name = get_firehose_delivery_stream()
    log_info(
        f"putting record to firehose delivery stream: {delivery_stream_name} record: {record}"
    )

    firehose.put_record(
        DeliveryStreamName=delivery_stream_name,
        Record={"Data": json.dumps(record)},
    )
