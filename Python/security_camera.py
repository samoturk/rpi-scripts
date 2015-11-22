import io
import sys
import time
import picamera
from PIL import Image
import argparse


def capture_image(resolution=(1024, 768), size=(320, 240), sleep=2):
    """
    Captures image from raspberry pi camera
    resolution -- resolution of capture
    size -- size of output
    sleep -- sleep time in seconds
    """
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        #camera.led = False
        camera.resolution = resolution
        camera.start_preview()
        time.sleep(sleep)
        camera.capture(stream, format='jpeg', resize=size)
    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    image = Image.open(stream)
    return image



def dhash(image, hash_size=8):
    """
    Calculates image hash
    Function found here (thanks!):
    http://blog.iconfinder.com/detecting-duplicate-images-using-python/
    image -- PIL image
    hash_size -- size of the hash that defines sensitivity
    """
    # Grayscale and shrink the image in one step.
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS,
    )

    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    # Convert the binary array to a hexadecimal string.
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0

    return ''.join(hex_string)

def record_images(folder, delay, duration, sensitivity, img_size, img_rotate):
    """
    Function that records images
    """
    hashes = []
    time_to_end = time.time() + duration*60
    while time.time() < time_to_end:
        image = capture_image(size=img_size, sleep=delay).rotate(img_rotate)
        if sensitivity == 'off':
            image.save(folder + "/" + time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time())) + "-" + '.jpeg', format='jpeg')
        else:
            hashx = dhash(image, hash_size=sensitivity)
            if hashx not in hashes:
                hashes.append(hashx)
                image.save(folder + "/" + time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time())) + "-" + hashx + '.jpeg', format='jpeg')
            
def arg_parser():
    parser = argparse.ArgumentParser(description='Raspberry Pi security camera. Takes images every few seconds (defined by delay) and \
                stores image only if it is dissimilar enough to previous images (defined by sensitivity).')
    parser.add_argument('-o', '--outfolder', help="Folder to save images to.")
    parser.add_argument('-d', '--delay', default=2, help="Delay between images in seconds (default:2).")
    parser.add_argument('-s', '--sensitivity', default=6, help="Hash size (default:6). If 'off' every image is stored.")
    parser.add_argument('-i', '--img_size', default="320:240", help="Image width:height - max 1024:786 (default:320:240).")
    parser.add_argument('-r', '--img_rotate', default=0, help="Image rotation in degrees (default:0).")
    parser.add_argument('-l', '--duration', default=10, help="Duration in minutes (default:10).")
    return parser

if __name__ == "__main__":
    parser = arg_parser()
    if len(sys.argv) == 1:
        argv = ['-h']
    else:
        argv = sys.argv[1:]
    args = parser.parse_args(argv)
    print(" Images will be saved in %s, \n Image will be taken every %s seconds for %s minutes,\
            \n Image resolution %s and rotation %s degrees, \n Hash sensitivity is %s" 
            %(args.outfolder, args.delay, args.duration, args.img_size, args.img_rotate, args.sensitivity))
    record_images(args.outfolder, float(args.delay), float(args.duration), int(args.sensitivity), 
                  (int(args.img_size.split(':')[0]), int(args.img_size.split(':')[1])), int(args.img_rotate))    
    print(" Recording finished..")


