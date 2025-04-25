#!/bin/bash

jetson-containers run -v $HOME/nevikw39/ASR/whisper:/mnt -e XDG_CACHE_HOME=/mnt/cache dustynv/whisper:r35.3.1 /mnt/serve.py $@
