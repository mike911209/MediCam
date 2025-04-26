#!/usr/bin/python3

import argparse
import logging
import json
import os
from pathlib import Path

import whisper

from interval import interval as Interval


def main(model_size: str, interval: float, waves_dir: str, texts_dir: str):
    model = whisper.load_model(model_size)
    options = whisper.DecodingOptions()

    logging.info(f"Model loaded.")

    @Interval(interval)
    def transcribe():
        for wave in os.listdir(waves_dir):
            wave_path = os.path.join(waves_dir, wave)

            logging.info(f"Transcribing {wave_path}...")

            audio = whisper.pad_or_trim(whisper.load_audio(wave_path))
            mel = whisper.log_mel_spectrogram(audio).to(model.device)
            result = whisper.decode(model, mel, options)

            with open(os.path.join(texts_dir, Path(wave).with_suffix(".json")), 'w') as f:
                logging.info(f"Saving to {wave_path}...")
                json.dump({"date": os.path.basename(wave_path), "text": result.text}, f)

            logging.info(f"Cleaning up {wave_path}...")
            os.remove(wave_path)

    try:
        transcribe()
    except Exception as e:
        logging.error(f"Error: {e}!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Whisper model launcher.")
    parser.add_argument(
        "--model_size",
        default="small",
        choices=("tiny", "base", "small", "medium", "large"),
    )
    parser.add_argument(
        "--interval",
        default=2.,
    )
    parser.add_argument(
        "--waves_dir",
        default="/mnt/waves",
    )
    parser.add_argument(
        "--texts_dir",
        default="/mnt/texts",
    )
    parser.add_argument(
        "--logging",
        default=0,
        type=int,
        choices=(0, 1, 2, 3, 4, 5),
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.logging * 10)

    main(args.model_size, args.interval, args.waves_dir, args.texts_dir)
