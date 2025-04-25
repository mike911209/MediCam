#!/usr/bin/python

import argparse
import os
import logging

from datetime import datetime

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav


SAMPLE_RATE = 16000  # Audio sample rate (Hz)
THRESHOLD = 1e-4  # Volume threshold to decide "not muted"


def main(waves_dir: str):
    while True:
        audio = sd.rec(30 * SAMPLE_RATE, samplerate=SAMPLE_RATE, channels=1)
        sd.wait()

        avg_vol = np.abs(audio).mean()
        logging.debug(f"avg. vol.: {avg_vol}")

        if avg_vol > THRESHOLD:
            wave_path = os.path.join(waves_dir, f"{datetime.now().strftime('%H%M%S_%f')}.wav")
            wav.write(wave_path, SAMPLE_RATE, (audio * 32767).astype(np.int16))
            logging.info(f"Saved {wave_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Whisper model launcher.")
    parser.add_argument(
        "--waves_dir",
        default="/home/icam-540/nevikw39/ASR/whisper/waves",
    )
    parser.add_argument(
        "--logging",
        default=0,
        type=int,
        choices=(0, 1, 2, 3, 4, 5),
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.logging * 10)

    main(args.waves_dir)
