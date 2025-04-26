import boto3
import datetime
import json

def lambda_handler(event, context):
    today = datetime.datetime.utcnow().date()
    today_str = today.strftime("%Y-%m-%d")

    bedrock_agent = boto3.client('bedrock-agent-runtime')

    response = bedrock_agent.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId='DailySummarySession',
        inputText=f"Please retrieve and summarize today's data ({today_str}) from the S3 bucket."
    )
    full_response = ""
    for event in response['completion']:
        if 'chunk' in event:
            chunk = event['chunk']['bytes'].decode('utf-8')
            full_response += chunk


    email_body = f"Daily Summary Report for {today_str}:\n\n{full_response}"

    sns = boto3.client('sns')
    sns.publish(
        TopicArn='arn:aws:sns:us-east-1:420210061761:DailySummary',
        Subject=f"Daily Summary - {today_str}",
        Message=email_body
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Daily summary sent successfully!')
    }