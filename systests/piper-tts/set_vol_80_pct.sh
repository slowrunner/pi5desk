#!/bin/bash

amixer -D pulse sset Master 80%
~/pi5desk/systests/piper-tts/piper.sh 'Volume set to 80 percent' 
