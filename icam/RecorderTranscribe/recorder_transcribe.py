#!/usr/bin/python

import argparse
import asyncio
import dotenv
import logging
import json

from datetime import datetime

from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler

import boto3
import sounddevice as sd


SAMPLE_RATE = 16000  # Audio sample rate (Hz)
BLOCK_SIZE = 1024 # Stream block size
THRESHOLD = 1e-4  # Volume threshold to decide "not muted"
BUCKET = "unapproved-orders"  # S3 bucket name


class Handler(TranscriptResultStreamHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.s3 = boto3.client("s3")

    async def handle_transcript_event(self, transcript_event):
        transcript = ''.join(result.alternatives[0].transcript for result in transcript_event.transcript.results if not result.is_partial and len(result.alternatives))
        if not transcript:
            logging.debug("No transcript.")
            return
        logging.debug(f"Transcript: {transcript}")
        print(transcript)

        name = datetime.now().isoformat(timespec="seconds")
        with open(f"/tmp/{name}.json", 'w') as f:
            json.dump({"date": name, "text": transcript}, f, ensure_ascii=False)
        self.s3.upload_file(f"/tmp/{name}.json", BUCKET, f"{name}.txt")


async def transcribe_streaming():
    ts = TranscribeStreamingClient(region="us-east-1")

    stream = await ts.start_stream_transcription(
        language_code="zh-TW",
        media_sample_rate_hz=SAMPLE_RATE,
        media_encoding="pcm"
    )
    
    handler = Handler(stream.output_stream)

    async def send():
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16", blocksize=BLOCK_SIZE) as device:
            while True:
                audio_chunk, _ = device.read(BLOCK_SIZE)
                await stream.input_stream.send_audio_event(audio_chunk=audio_chunk.tobytes())

    async def receive(): await handler.handle_events()

    await asyncio.gather(send(), receive())


def main(): asyncio.run(transcribe_streaming())


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
