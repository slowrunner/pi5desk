TTS Piper

REF: https://github.com/rhasspy/piper  
REF: https://www.youtube.com/watch?v=rjq5eZoWWSo  




1) Install for Python  
```
pip3 install piper-tts  

sudo pip3 install piper-tts --break-system-packages  
```

Try it (will download the voices to the cwd:  
```
echo 'Welcome to the world of speech synthesis!' | piper \  
  --model en_US-lessac-medium \  
  --output_file welcome.wav   

echo 'Welcome to the world of speech synthesis!' | piper   --model en_US-lessac-medium.onnx    --output_raw | aplay -r 22050 -f S16_LE -t raw -   


$ piper -h  
usage: piper [-h] -m MODEL [-c CONFIG] [-f OUTPUT_FILE] [-d OUTPUT_DIR] [--output-raw] [-s SPEAKER] [--length-scale LENGTH_SCALE]  
             [--noise-scale NOISE_SCALE] [--noise-w NOISE_W] [--cuda] [--sentence-silence SENTENCE_SILENCE] [--data-dir DATA_DIR]  
             [--download-dir DOWNLOAD_DIR] [--update-voices] [--debug]  

options:  
  -h, --help            show this help message and exit  
  -m MODEL, --model MODEL  
                        Path to Onnx model file  
  -c CONFIG, --config CONFIG  
                        Path to model config file  
  -f OUTPUT_FILE, --output-file OUTPUT_FILE, --output_file OUTPUT_FILE  
                        Path to output WAV file (default: stdout)
  -d OUTPUT_DIR, --output-dir OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Path to output directory (default: cwd)
  --output-raw, --output_raw
                        Stream raw audio to stdout
  -s SPEAKER, --speaker SPEAKER
                        Id of speaker (default: 0)
  --length-scale LENGTH_SCALE, --length_scale LENGTH_SCALE
                        Phoneme length
  --noise-scale NOISE_SCALE, --noise_scale NOISE_SCALE
                        Generator noise
  --noise-w NOISE_W, --noise_w NOISE_W
                        Phoneme width noise
  --cuda                Use GPU
  --sentence-silence SENTENCE_SILENCE, --sentence_silence SENTENCE_SILENCE
                        Seconds of silence after each sentence
  --data-dir DATA_DIR, --data_dir DATA_DIR
                        Data directory to check for downloaded models (default: current directory)
  --download-dir DOWNLOAD_DIR, --download_dir DOWNLOAD_DIR
                        Directory to download voices into (default: first data dir)
  --update-voices       Download latest voices.json during startup
  --debug               Print DEBUG messages to console


$ amixer scontents  (Shows default volume 40%)
Simple mixer control 'Master',0
  Capabilities: pvolume pswitch pswitch-joined
  Playback channels: Front Left - Front Right
  Limits: Playback 0 - 65536
  Mono:
  Front Left: Playback 26304 [40%] [on]
  Front Right: Playback 26304 [40%] [on]
Simple mixer control 'Capture',0
  Capabilities: cvolume cswitch cswitch-joined
  Capture channels: Front Left - Front Right
  Limits: Capture 0 - 65536
  Front Left: Capture 65536 [100%] [on]
  Front Right: Capture 65536 [100%] [on]

```

** increase volume:
```
  amixer -D pulse sset Master 80%
```

** get arctic-medium voice for wali  (downloads it then uses it)
```
echo 'Welcome to the world of speech synthesis!' | piper  --model en_US-arctic-medium     --output_file arctic-medium.wav
```

** piper.sh to play arctic voice 
```
#!/bin/bash

pushd /home/pi/pi5desk/systests/piper-tts
echo $1 | piper   --model en_US-arctic-medium.onnx    --output_raw | aplay -r 22050 -f S16_LE -t raw - 
popd
```

** ALSO CAN INSTALL DIRECT
```
1) Create piper folder, cd to it
mkdir piper
cd piper

2) Download 64-bit RPi image: 
  wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz

3) Unzip
tar -xvzf piper_arm64.tar.gz

4) Try it:
echo 'This sentence is spoken first. This sentence is synthesized while the first sentence is spoken.' | \
  ./piper --model en_US-lessac-medium.onnx --output-raw | \
  aplay -r 22050 -f S16_LE -t raw -

```

