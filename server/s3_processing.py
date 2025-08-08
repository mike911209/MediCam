import json
import boto3

s3 = boto3.client('s3')
polly = boto3.client('polly')
iot_client = boto3.client('iot-data', region_name='us-east-1')
bedrock_agent = boto3.client('bedrock-agent-runtime')
AGENT_ID = "TFLUWBXBC1"
AGENT_ALIAS_ID = "YIBAITDYIP"

audio_bucket = "audio-response"

def lambda_handler(event, context):
    # Get bucket name and object key from the event
    sns_message = event['Records'][0]['Sns']['Message']
    s3_event = json.loads(sns_message)

    bucket_name = s3_event['Records'][0]['s3']['bucket']['name']
    object_key = s3_event['Records'][0]['s3']['object']['key']
    
    # Fetch the object from S3
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    
    # Read the object's content
    content = response['Body'].read().decode('utf-8')
    content = content.lower()
    
    if "medica" in content:
        response = bedrock_agent.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId='Damn',
            inputText=content
        )

        full_response = ""
        for event in response['completion']:
            if 'chunk' in event:
                chunk = event['chunk']['bytes'].decode('utf-8')
                full_response += chunk
        
        print(f"agent response: {full_response}")

        polly_response = polly.synthesize_speech(
            Text=full_response,
            OutputFormat='mp3',
            VoiceId='Joanna'
        )

        audio_key = object_key.replace('.txt', '.mp3')

        s3.put_object(
            Bucket=audio_bucket,
            Key=audio_key,
            Body=polly_response['AudioStream'].read(),
            ContentType='audio/mpeg'
        )
    

    response = iot_client.publish(
        topic='icam/audio_response',
        qos=1,
        payload=json.dumps({
            'bucket': audio_bucket,
            'key': audio_key,
        })
    )

    return {
        'statusCode': 200,
        'body': json.dumps('File processed successfully!')
    }
