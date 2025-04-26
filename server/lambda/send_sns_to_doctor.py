import json
import boto3
import urllib.parse
import os

SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")
APPROVE_INVOKE_BASE_URL = os.getenv("APPROVE_INVOKE_BASE_URL")


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    sns = boto3.client("sns")

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )

    s3_response = s3.get_object(Bucket=bucket, Key=object_key)
    file_content = s3_response["Body"].read().decode("utf-8")
    data = json.loads(file_content)

    email_body = "New Order Received:\n\n"
    for key, value in data.items():
        email_body += f"{key}: {value}\n"

    approve_link = f"{APPROVE_INVOKE_BASE_URL}?object_key={object_key}"
    email_body += f"\n\nClick here to approve the order 👉 {approve_link}"

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="Medical Order Approval Needed",
        Message=email_body,
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            "Successfully processed new JSON file(s) and sent email(s)!"
        ),
    }
