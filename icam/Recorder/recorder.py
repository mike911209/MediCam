#!/usr/bin/python

import argparse
import dotenv
import logging
import os

from datetime import datetime

import boto3
import numpy as np
import scipy.io.wavfile as wav
import sounddevice as sd

from interval import interval as Interval


SAMPLE_RATE = 16000  # Audio sample rate (Hz)
THRESHOLD = 1e-4  # Volume threshold to decide "not muted"
BUCKET = "audio-bucket-aws-hackathon"  # S3 bucket name


def main(interval: float, waves_dir: str, texts_dir: str):
    s3 = boto3.client("s3")

    @Interval(interval)
    def upload():
        for text in os.listdir(texts_dir):
            text_path = os.path.join(texts_dir, text)

            logging.info(f"Uploading {text_path}...")
            s3.upload_file(text_path, BUCKET, "kb/" + text)

            logging.info(f"Cleaning up {text_path}...")
            os.remove(text_path)

    upload()

    while True:
        audio = sd.rec(30 * SAMPLE_RATE, samplerate=SAMPLE_RATE, channels=1)
        sd.wait()

        avg_vol = np.abs(audio).mean()
        logging.debug(f"avg. vol.: {avg_vol}")

        if avg_vol > THRESHOLD:
            wave_path = os.path.join(waves_dir, f"{datetime.now().isoformat(timespec='seconds')}.wav")
            wav.write(wave_path, SAMPLE_RATE, (audio * 32767).astype(np.int16))
            logging.info(f"Saved {wave_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recorder.")
    parser.add_argument(
        "--interval",
        default=2.,
    )
    parser.add_argument(
        "--waves_dir",
        default="/home/icam-540/nevikw39/ASR/whisper/waves",
    )
    parser.add_argument(
        "--texts_dir",
        default="/home/icam-540/nevikw39/ASR/whisper/texts",
    )
    parser.add_argument(
        "--logging",
        default=0,
        type=int,
        choices=(0, 1, 2, 3, 4, 5),
    )
    args = parser.parse_args()

    dotenv.load_dotenv()

    logging.basicConfig(level=args.logging * 10)

    main(args.interval, args.waves_dir, args.texts_dir)
