import json
import urllib.parse
import urllib3
import boto3
import os
import smtplib
from email.mime.text import MIMEText

APPROVE_INVOKE_BASE_URL = "https://mey7i7fmo6.execute-api.us-east-1.amazonaws.com/doctor/get_response"
import requests
from requests_aws4auth import AWS4Auth
from urllib.parse import urlparse
def lambda_handler(event, context):

    session = boto3.Session()
    credentials = session.get_credentials()
    if credentials is None:
        raise Exception("❌ No AWS credentials found.")
    credentials = credentials.get_frozen_credentials()
    http = urllib3.PoolManager()
    awsauth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        'us-east-1',
        'aoss',
        session_token=credentials.token
    )

    sns_message = event['Records'][0]['Sns']['Message']
    s3_event = json.loads(sns_message)
    s3 = boto3.client('s3')
    bucket_name = "unapproved-orders"
    object_key = s3_event['Records'][0]['s3']['object']['key']

    embedding_bucket = "face-embedding"

    text_response = s3.get_object(Bucket=bucket_name, Key=object_key)
    text_content = text_response['Body'].read().decode('utf-8')

    embedding_response = s3.get_object(Bucket=embedding_bucket, Key=object_key)
    embedding_content = embedding_response['Body'].read().decode('utf-8')

    embedding_list = json.loads(embedding_content)
    no_doctor = True
    for embedding in embedding_list:
        name, email = query_embedding(embedding,awsauth)
        if name is not None:
            no_doctor = False
            print(f"Found person: {name} with email: {email}")
            gmail_user = 'ayaba7077@gmail.com'
            gmail_password = 'echs rsyu ugjx nnti'
            bucket = "unapproved-orders"
            s3_response = s3.get_object(Bucket=bucket, Key=object_key)
            file_content = s3_response["Body"].read().decode("utf-8")
            data = json.loads(file_content)
            
            email_body = f"Dear {name}, here is the new Order Received:\n\n"
            for key, value in data.items():
                email_body += f"{key}: {value}\n"

            approve_link = f"{APPROVE_INVOKE_BASE_URL}?object_key={object_key}&ismurmur={'false'}"
            email_body += f"\n\nClick here to approve the order 👉 {approve_link}"

            msg = MIMEText(email_body)
            msg['Subject'] = "Medical Order Approval Needed"
            msg['From'] = gmail_user
            msg['To'] = email

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(gmail_user, gmail_password)
                server.send_message(msg)
            break
    print(no_doctor)
    if no_doctor:
        approve_link = f"{APPROVE_INVOKE_BASE_URL}?object_key={object_key}&ismurmur={'true'}"
        response = http.request('GET', approve_link)

def query_embedding(embedding,awsauth, score_threshold=0.3):
    index_name = 'faces-v3'
    collection_endpoint = 'https://oc6h1mvaevky0loj0xaa.us-east-1.aoss.amazonaws.com'  # 不要有 https://
    search_url = f"{collection_endpoint}/{index_name}/_search"
    query = {
        "size": 1,
        "query": {
            "knn": {
                "embeddings": {
                    "vector": embedding,
                    "k": 1
                }
            }
        }
    }
    response = requests.post(
        search_url,
        auth=awsauth,
        json=query,
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 200:
        hits = response.json()["hits"]["hits"]
        name = hits[0]["_source"]["name"] if hits else None
        email = hits[0]["_source"]["mail"] if hits else None
        score = hits[0]["_score"] if hits else None
        print(f"score: {score}")
        if score < score_threshold:
            return None,None
        else:
            return name ,email
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None,None
