import json
import uuid
import boto3


def lambda_handler(event, context):
    bedrock_agent = boto3.client('bedrock-agent-runtime')

    body = json.loads(event["body"])
    input_text = body.get("input", "")
    session_id = body.get("sessionId") or str(uuid.uuid4())

    response = bedrock_agent.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId=session_id,
        inputText=input_text
    )

    full_response = ""
    for event in response['completion']:
        if 'chunk' in event:
            chunk = event['chunk']['bytes'].decode('utf-8')
            full_response += chunk
    return {
        'statusCode': 200,
        'body': json.dumps(full_response)
    }
