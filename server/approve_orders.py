import boto3
import urllib.parse

s3 = boto3.client('s3')

def lambda_handler(event, context):
    params = event['queryStringParameters']
    src_bucket = 'unapproved-orders'
    src_key = urllib.parse.unquote_plus(params['object_key'])
    ismurmur = params['ismurmur']

    dest_bucket = 'approved-orders'
    dest_key = src_key if ismurmur == 'true' else 'kb/' + src_key

    s3.copy_object(
        Bucket=dest_bucket,
        CopySource={'Bucket': src_bucket, 'Key': src_key},
        Key=dest_key
    )

    s3.delete_object(Bucket=src_bucket, Key=src_key)

    return {
    'statusCode': 200,
    'headers': {
        'Content-Type': 'text/html'
    },
    'body': """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Approval Complete</title></head><body><h1>✅ The medical order has been successfully approved.</h1><p>You may now close this page.</p></body></html>"""
}
