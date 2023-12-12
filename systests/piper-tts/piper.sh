#!/bin/bash


pushd /home/pi/pi5desk/systests/piper-tts
echo $1 | piper   --model en_US-arctic-medium.onnx    --output_raw | aplay -r 22050 -f S16_LE -t raw - 
popd
