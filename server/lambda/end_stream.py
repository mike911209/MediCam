import boto3
import json

def lambda_handler(event, context):
    iot_client = boto3.client('iot-data', region_name='us-east-1')  # change to your region

    response = iot_client.publish(
        topic='icam/end_stream',  # same topic the device is subscribed to
        qos=1,
        payload=json.dumps({
            'end_stream': True,
        })
    )

    return {
        'statusCode': 200,
        'body': 'End Streaming'
    }
