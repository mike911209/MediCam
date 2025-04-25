import os
from dotenv import load_dotenv
from subprocess import Popen

load_dotenv(override=True)

class Config:
    region = os.getenv("AWS_DEFAULT_REGION")
    stream_name = os.getenv("KVS_STREAM_NAME")

    api_prefix = "http://localhost:5000"
    connect_prefix = "/home/icam-540/Dev/connect/"

    # Device credentials (downloaded from AWS IoT Core)
    cert_filepath = connect_prefix + "icam.cert.pem"
    key_filepath = connect_prefix + "icam.private.key"
    ca_filepath = connect_prefix + "root-CA.crt"

    iot_client_id = "icam"
    iot_endpoint = "a30nuhpd8lu11l-ats.iot.us-east-1.amazonaws.com"

    process: Popen = None
