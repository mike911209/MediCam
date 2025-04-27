#!/usr/bin/python

import argparse
import dotenv
import io
import json
import logging
import os

from datetime import datetime

import boto3
import numpy as np
import scipy.io.wavfile as wav
import sounddevice as sd

from sagemaker.jumpstart import utils

from detect import FaceRecognition


SAMPLE_RATE = 16000  # Audio sample rate (Hz)
THRESHOLD = 1e-4  # Volume threshold to decide "not muted"
BUCKET = "unapproved-orders"  # S3 bucket name
BUCKET_FE = "face-embedding"  # S3 bucket name
endpoint_name = 'jumpstart-dft-hf-asr-whisper-large-20250427-010006'


def main():
    s3 = boto3.client("s3")
    sagemaker = boto3.client('runtime.sagemaker')

    fr = FaceRecognition("yolov11n-face.pt")

    def get_embeddings():
        try:
            fr.process_frame(fr.get_frame())
            bytes = json.dumps(list(map(lambda x: x.tolist(), fr.embeddings)), ensure_ascii=False).encode("utf-8")
            return io.BytesIO(bytes)
        except Exception as e:
            logging.error(f"Error: {e}!!")
            return None

    logging.info(f"Starting!!")

    while True:
        embeddings = get_embeddings()
        audio = sd.rec(15 * SAMPLE_RATE, samplerate=SAMPLE_RATE, channels=1)
        sd.wait()

        name = datetime.now().isoformat(timespec="seconds").replace(':', '_')
        wav.write(f"/tmp/{name}.wav", SAMPLE_RATE, (audio * 32767).astype(np.int16))
        logging.info(f"Saved {name}.")

        with open(f"/tmp/{name}.wav", "rb") as f:
            bytes = f.read()

        response = sagemaker.invoke_endpoint(EndpointName=endpoint_name, ContentType="audio/wav", Body=bytes)

        model_predictions = json.loads(response['Body'].read())
        text = model_predictions['text'][0].strip()

        if text and text != "you":
            logging.info(f"Text: {text}")
            bytes = json.dumps({"date": name, "text": text}, ensure_ascii=False).encode("utf-8")
            file_obj = io.BytesIO(bytes)
            s3.upload_fileobj(file_obj, BUCKET, f"{name}.json")
            if embeddings != None:
                s3.upload_fileobj(embeddings, BUCKET_FE, f"{name}.json")
        else:
            logging.info(f"Empty?")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recorder with SageMaker JumpStart.")
    parser.add_argument(
        "--logging",
        default=0,
        type=int,
        choices=(0, 1, 2, 3, 4, 5),
    )
    args = parser.parse_args()

    dotenv.load_dotenv()

    logging.basicConfig(level=args.logging * 10)

    main()
