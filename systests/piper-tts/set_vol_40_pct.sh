#!/bin/bash

amixer -D pulse sset Master 40%
~/pi5desk/systests/piper-tts/piper.sh 'Volume set to 40 percent'
