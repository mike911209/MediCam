#!/usr/bin/python

import argparse
import dotenv
import logging
import json
import os
import time
import requests

from datetime import datetime

import boto3
import numpy as np
import scipy.io.wavfile as wav
import sounddevice as sd


SAMPLE_RATE = 16000  # Audio sample rate (Hz)
THRESHOLD = 1e-4  # Volume threshold to decide "not muted"
BUCKET_TEXT = "unapproved-orders"  # S3 bucket name
BUCKET_RECORDING = "medicam-recordings"  #


def main():
    s3 = boto3.client("s3")
    transcribe = boto3.client('transcribe')

    while True:
        audio = sd.rec(10 * SAMPLE_RATE, samplerate=SAMPLE_RATE, channels=1)
        sd.wait()

        avg_vol = np.abs(audio).mean()
        logging.debug(f"avg. vol.: {avg_vol}")

        if True: # avg_vol > THRESHOLD:
            job = datetime.now().isoformat(timespec="seconds").replace(':', '-')
            path = f"/tmp/{job}.wav"

            logging.info(f"Saving {path}...")
            wav.write(path, SAMPLE_RATE, (audio * 32767).astype(np.int16))

            logging.info(f"Uploading {path}...")
            s3.upload_file(path, BUCKET_RECORDING, f"{job}.wav")

            logging.info(f"Transcribing {path}...")
            transcribe.start_transcription_job(
                TranscriptionJobName=job,
                Media={'MediaFileUri': f"s3://{BUCKET_RECORDING}/{job}.wav"},
                MediaFormat='wav',
                IdentifyMultipleLanguages=True,
                LanguageOptions=('en-US', 'zh-TW'),
            )

            while (result := transcribe.get_transcription_job(TranscriptionJobName=job))['TranscriptionJob']['TranscriptionJobStatus'] not in ('COMPLETED', 'FAILED'):
                time.sleep(2)
            
            if result['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED':
                logging.error(f"Transcription failed: {result['TranscriptionJob']['FailureReason']}!!")
                continue

            url = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
            response = requests.get(url).json()['results']['transcripts'][0]['transcript']
            logging.debug(f"response: {response}")
            
            with open(f"/tmp/{job}.json", 'w') as f:
                json.dump({"date": job, "text": response}, f)
            s3.upload_file(f"/tmp/{job}.json", BUCKET_TEXT, f"{job}.json")

            logging.info(f"Cleaning up {job}...")
            os.remove(f"/tmp/{job}.wav")
            os.remove(f"/tmp/{job}.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recorder with Transcribe.")
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
