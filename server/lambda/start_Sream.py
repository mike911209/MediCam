import boto3
import json

def lambda_handler(event, context):
    iot_client = boto3.client('iot-data', region_name='us-east-1')  # change to your region

    response = iot_client.publish(
        topic='icam/start_stream',  # same topic the device is subscribed to
        qos=1,
        payload=json.dumps({
            'start_stream': True,
            'led_status': '3',
        })
    )

    return {
        'statusCode': 200,
        'body': 'Start Streaming!'
    }
