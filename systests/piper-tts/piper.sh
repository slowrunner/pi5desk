#!/bin/bash


pushd /home/pi/pi5desk/systests/piper-tts
echo $1 | piper   --model en_US-arctic-medium.onnx    --output_raw | aplay -r 33075 -f S16_LE -t raw - 
popd
