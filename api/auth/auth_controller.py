import json
from core_lib.utils.log_util import log_info
from api_lib.auth.authorization import authorize


def authenticate(event, context):
    log_info("log test")
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
            }
        ),
    }
