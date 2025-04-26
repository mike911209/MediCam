#!/bin/bash

jetson-containers run -v $HOME/nevikw39/ASR/whisper:/mnt dustynv/whisper_trt:r36.3.0 /mnt/serve_trt.py $@
