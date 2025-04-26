import os
from awscrt import io, mqtt
from awscrt.mqtt import Connection
from awsiot import mqtt_connection_builder
from loguru import logger
import json
import requests
import subprocess
from config import Config
import signal
import boto3
import tempfile

s3 = boto3.client('s3')

def mqtt_build() -> Connection:
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)

    # MQTT client setup
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=Config.iot_endpoint,
        cert_filepath=Config.cert_filepath,
        pri_key_filepath=Config.key_filepath,
        client_bootstrap=io.ClientBootstrap(event_loop_group, host_resolver),
        ca_filepath=Config.ca_filepath,
        client_id=Config.iot_client_id,
        clean_session=True,
        keep_alive_secs=30
    )

    # Connect
    logger.info("Connecting...")
    mqtt_connection.connect().result()
    logger.success("Connected!")

    return mqtt_connection

def start_streaming() -> subprocess.Popen:
    # GStreamer pipeline: test source → h264 encode → send to KVS
    # turn the following command into a python subprocess

    command = [
        "gst-launch-1.0",
        "v4l2src", "do-timestamp=TRUE", "device=/dev/video10", "!",
        "videoconvert", "!",
        "video/x-raw,format=I420,width=640,height=480,framerate=30/1", "!",
        "x264enc", "bframes=0", "key-int-max=30", "bitrate=500", "tune=zerolatency", "!",
        "h264parse", "!",
        "video/x-h264,stream-format=avc,alignment=au,profile=baseline", "!",
        "kvssink",
        f"stream-name={Config.stream_name}",
        f"storage-size=512",
        f"fragment-duration=2000"
    ]
    process = subprocess.Popen(command, env=os.environ.copy())

    return process

def subscribe(mqtt_connection: Connection):
    # api for start streaming
    def start_stream(topic, payload, **kwargs):
        message = json.loads(payload)
        print("inside start stream")
        if message["start_stream"]:
            logger.info("Start streaming...")

            led_status = message["led_status"] if "led_status" in message else '0'
            response = requests.post(Config.api_prefix + "/camera/led_status", files={
                'led_status': (None, led_status)
            })
            if response.status_code != 200:
                logger.debug(response.text)
                logger.error("Streaming failed due to led error")
            
            response = requests.post(Config.api_prefix + "/camera/play")
            if response.status_code != 200:
                logger.debug(response.text)
                logger.error("Streaming failed due to camera error")

            Config.process = start_streaming()

            logger.success("Streaming started")

    mqtt_connection.subscribe(
        topic="icam/start_stream",
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=start_stream
    )

    # api for stop streaming
    def end_stream(topic, payload, **kwargs):
        message = json.loads(payload)
        if message["end_stream"]:
            logger.info("Ending streaming...")

            led_status = '0'
            response = requests.post(Config.api_prefix + "/camera/led_status", files={
                'led_status': (None, led_status)
            })
            if response.status_code != 200:
                logger.error("Pausing streaming failed due to led error")
            
            response = requests.post(Config.api_prefix + "/camera/pause")
            if response.status_code != 200:
                logger.error("Pausing streaming failed due to camera error")

            Config.process.terminate()
            
            logger.success("Streaming ended")

    mqtt_connection.subscribe(
        topic="icam/end_stream",
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=end_stream
    )

    def play_audio(topic, payload, **kwargs):
        logger.info("Start playing audio")
        message = json.loads(payload)
        bucket_name = message["bucket"]
        key = message["key"]

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file_path = tmp_file.name
            s3.download_fileobj(Bucket=bucket_name, Key=key, Fileobj=tmp_file)

        logger.info(f"Downloaded audio to {tmp_file_path}")

        try:
            subprocess.run(['mpg123', tmp_file_path], check=True)
            logger.info("Audio played successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to play audio: {e}")

        logger.info("Done played audio")
    
    mqtt_connection.subscribe(
        topic="icam/audio_response",
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=play_audio
    )

if __name__ == "__main__":
    logger.info("Starting streaming...")
    mqtt_connection = mqtt_build()

    subscribe(mqtt_connection)
    
    signal.pause()