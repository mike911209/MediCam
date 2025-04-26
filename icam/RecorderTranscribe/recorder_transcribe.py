#!/usr/bin/python

import argparse
import asyncio
import dotenv
import io
import json
import logging

from datetime import datetime

from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler

import boto3
import sounddevice as sd


SAMPLE_RATE = 16000  # Audio sample rate (Hz)
BLOCK_SIZE = 2048  # Stream block size
BUCKET = "unapproved-orders"  # S3 bucket name


class Handler(TranscriptResultStreamHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.s3 = boto3.client("s3")
        self.buffer = []
        self.counter = 0

    async def handle_transcript_event(self, transcript_event):
        transcript = ''.join(
            result.alternatives[0].transcript
            for result in transcript_event.transcript.results
            if not result.is_partial and len(result.alternatives)
        ).strip()

        if transcript:
            self.counter = 0
            self.buffer.append(transcript)
            logging.debug(f"Transcript: {transcript}")
        elif self.buffer:
            self.counter += 1
            if self.counter > 64:
                self.counter = 0
                logging.info("Uploading...")
                name = datetime.now().isoformat(timespec="seconds")
                bytes = json.dumps({"date": name, "text": ' '.join(self.buffer)}, ensure_ascii=False).encode("utf-8")
                file_obj = io.BytesIO(bytes)
                self.s3.upload_fileobj(file_obj, BUCKET, f"{name}.json")
                self.buffer.clear()


async def transcribe_streaming():
    ts = TranscribeStreamingClient(region="us-east-1")

    stream = await ts.start_stream_transcription(
        language_code=None,
        media_sample_rate_hz=SAMPLE_RATE,
        media_encoding="pcm",
        identify_multiple_languages=True,
        language_options=("zh-TW", "en-US"),
    )
    
    handler = Handler(stream.output_stream)

    async def send():
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16", blocksize=BLOCK_SIZE) as device:
            while True:
                audio_chunk, _ = device.read(BLOCK_SIZE)
                await stream.input_stream.send_audio_event(audio_chunk=audio_chunk.tobytes())

    async def receive(): await handler.handle_events()

    logging.info("Starting...")

    await asyncio.gather(send(), receive())


def main(): asyncio.run(transcribe_streaming())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recorder with Transcribe Stream.")
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
