#!/bin/bash

## This bash script calls a python script which outputs picamera
## output to stdout, this script then pipes that through ffmpeg to
## stream to uStream
 
while :
do
#  python3 cameraStreamBash.py | ffmpeg -i - -vcodec copy -an -metadata title="Streaming from raspberry pi camera" -f flv $RTMP_URL/$STREAM_KEY
  python3 cameraStreamBash.py | nc -lkv4 8080
  sleep 2
done
