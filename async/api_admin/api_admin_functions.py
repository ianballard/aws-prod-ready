import json
from datetime import datetime

from core_lib.utils.cloudformation_custom_resource_util import send_cfn_response
from core_lib.utils.lambda_util import lambda_handler
from core_lib.utils.thread_util import safe_get_thread_attribute
from core_lib.utils.log_util import log_unexpected_exception, log_warning
from core_lib.services.file_storage import file_storage_service
import boto3

api_gateway_client = boto3.client("apigateway")
cloudfront_client = boto3.client('cloudfront')


@lambda_handler()
def manage_api_exports(event):
    api_id = event.get("ResourceProperties", {}).get("ApiId")
    bucket_name = event.get("ResourceProperties", {}).get("BucketName")
    cloud_front_dist = event.get("ResourceProperties", {}).get("CloudFrontDistribution")
    api_url = event.get("ResourceProperties", {}).get("ApiUrl")
    if event.get("RequestType") in ["Create", "Update"] and api_id and bucket_name:

        try:

            file_key = get_api_file_key(api_id=api_id)
            if not file_key:
                log_warning(f"api not found: {api_id}")

            api_definition = get_export_content(api_id=api_id).decode('utf-8')

            if not api_definition:
                log_warning(f"unable to export: {api_id}")

            api_definition_json = json.loads(api_definition)

            api_definition_json['servers'] = [
                {
                    "url": api_url
                }
            ]

            file_storage_service.upload(
                bucket_name=bucket_name, key=file_key, content=json.dumps(api_definition_json)
            )

            create_invalidation(distribution_id=cloud_front_dist)

        except Exception as e:
            log_unexpected_exception(e)

    send_cfn_response(
        event,
        safe_get_thread_attribute("context"),
        "SUCCESS",
        {"Message": "Lambda function triggered"},
    )


def get_export_content(api_id: str):
    try:
        export_response = api_gateway_client.get_export(
            restApiId=api_id,
            stageName="Prod",
            exportType="oas30",
            accepts="application/json",
        )

        return export_response["body"].read()

    except Exception as e:
        log_unexpected_exception(e)


def get_api_file_key(api_id: str):
    try:
        api = api_gateway_client.get_rest_api(restApiId=api_id)

        description = api.get("description")

        file_key = f"{description}.json"

        return file_key

    except Exception as e:
        log_unexpected_exception(e)


def create_invalidation(distribution_id: str):
    try:
        return cloudfront_client.create_invalidation(
            DistributionId=distribution_id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': 1,
                    'Items': [
                        '/*',
                    ]
                },
                'CallerReference': str(datetime.utcnow())
            }
        )
    except Exception as e:
        log_unexpected_exception(e)


def get_distribution(distribution_id: str):
    try:
        return cloudfront_client.get_distribution(
            Id=distribution_id
        ).get('Distribution')
    except Exception as e:
        log_unexpected_exception(e)
