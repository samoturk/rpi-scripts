# rpi-scripts
Different scripts for Raspberry Pi

## Folder Python

### security_camera.py
Script that makes RPi with RPi camera a security device. I recommend running it with cron.  
It depends on PIL and picamera packages.
```bash
usage: security_camera.py [-h] [-o OUTFOLDER] [-d DELAY] [-s SENSITIVITY]
                          [-i IMG_SIZE] [-r IMG_ROTATE] [-l DURATION]

Raspberry Pi security camera. Takes images every few seconds (defined by
delay) and stores image only if it is dissimilar enough to previous images
(defined by sensitivity).

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFOLDER, --outfolder OUTFOLDER
                        Folder to save images to.
  -d DELAY, --delay DELAY
                        Delay between images in seconds (default:2).
  -s SENSITIVITY, --sensitivity SENSITIVITY
                        Hash size (default:6). If 'off' every image is stored.
  -i IMG_SIZE, --img_size IMG_SIZE
                        Image width:height - max 1024:786 (default:320:240).
  -r IMG_ROTATE, --img_rotate IMG_ROTATE
                        Image rotation in degrees (default:0).
  -l DURATION, --duration DURATION
                        Duration in minutes (default:10).
```