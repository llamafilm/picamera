#!/usr/bin/env python3

## This Python script sends picamera video output to stout,
## it is intended to be called from a bash script which pipes
## the output into ffmpeg.
## Bash script is startPythonStream.sh

import os
import time
import picamera
import sys
#from signal import pause
from gpiozero import CPUTemperature

def getStats():
# CPU temp
    cpu = CPUTemperature()
    stats = '  /  ' + str(round(cpu.temperature,1)) + '\'C'
    # uptime
    with open('/proc/uptime', 'r') as f:
      uptime_seconds = int(float(f.readline().split()[0]))
    m, s = divmod(uptime_seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    upstring = '%d days, %d:%02d' % (d, h, m)
    stats += '  /  up ' + upstring + '  /  ' + str(os.getloadavg())
    return stats

sys.stdout = os.fdopen(sys.stdout.fileno(), 'wb', 0)

## Start capturing video
with picamera.PiCamera() as camera:
  camera.resolution = (1280, 720)
  camera.sensor_mode = 0
  camera.framerate = 24
  camera.rotation = 180
  camera.annotate_foreground = picamera.Color(y=.5, u=0, v=0)
  camera.annotate_background = True
#  camera.iso = 1600
#  camera.exposure_mode = 'nightpreview'
  camera.start_recording(sys.stdout, bitrate = 1000000, format='h264')

  # Add text overlays.  Time updates every 0.2ms and stats update every 2s
  stats_frequency = 2
  start = time.time()
  last = start
  annotation = getStats()
  while True:
    current_time = time.strftime('%H:%M:%S')
    if time.time() - last > 2:
      annotation = getStats()
      last = time.time()
    camera.annotate_text = current_time + annotation
    camera.wait_recording(0.2)
#  pause()
#  input()
