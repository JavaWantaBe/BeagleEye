__author__ = 'richard'

import cv2
import database
import logging
from os import path
import direction
import icu
import ocr
import time
from settings import SettingManager
import sys
from capmanager import CaptureManager

on_beaglebone = True

try:
    import Adafruit_BBIO.GPIO as GPIO
except ImportError:
    on_beaglebone = False

# *********************Settings Mangaer******************
#   Settings manager
local_settings = SettingManager()

# ********************** Logger **************************
#   Create logger with proper date and formatting for both
#   file system and console
logging.basicConfig(level=logging.DEBUG,
                    format=('%(asctime)s %(name)-6s %(levelname)-4s %(message)s'),
                    datefmt='%m-%d %H:%M',
                    filename= path.join('log', 'system.log'),
                    filemode='a')
# Setup file handler
fh = logging.FileHandler('log/system.log')
fh.setLevel(logging.DEBUG)

# Setup console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Setup format of logger output
consoleFormat = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
ch.setFormatter(consoleFormat)

# Add handlers to logger
logging.getLogger('').addHandler(ch)

# Create logger for this module
syslog = logging.getLogger('main')


# ******************************************
#               Functions
# ******************************************
def print_usage():
    print """Usage: python beagleeye.py [h|l|u]
    h: http video file
    l: local video file
    u: usb or integrated camera device"""
    exit(1)


def main():
    # *********************Web Video ************************
    #   The video file mjpg/video.mjpg is simply being accessed
    #   on a http server (this is a live feed)
    http_video_file = "http://myapplecam.com/mjpg/video.mjpg"

    argument_length = len(sys.argv)
    cam_settings = local_settings.get_settings('camera')
    capture_device = 0

    if argument_length >= 2:
        # if there is a supplied argument, make sure there is only one
        if sys.argv[1] == 'h':
            capture_device = CaptureManager(http_video_file, 100)
        elif sys.argv[1] == 'l':
            try:
                capture = sys.argv[2]
            except IndexError:
                print_usage()
            if not path.isfile(capture):
                print "File Not found"
                print_usage()
            capture_device = CaptureManager(capture, 100)
        elif sys.argv[1] == 'u':
            try:
                capture = int(sys.argv[2])
            except IndexError:
                capture = 0
            if not isinstance(capture, (int, long)):
                print_usage()
            capture_device = CaptureManager(capture, 100, int(cam_settings['fps']))
            capture_device.set_dimensions(int(cam_settings['height']), int(cam_settings['width']))
        else:
            print_usage()
            exit(1)

    detected_movement = False   # Variable for determining when to exit loop
    # on_beaglebone = False

    syslog.info("system started")
    capture_device.start()

    time.sleep(2)

    while True:
        # Check if coming or going
        while not detected_movement:
#            direction.find_average(capture_device.get_queue)
            time.sleep(2)
            if capture_device.get_size() >= 10:
                print "going to detection"
                direction.w_find_direction(capture_device.get_queue, capture_device.get_size())
            else:
                print "frames: ", capture_device.get_size()
        detected_movement = False

        # If check equals setting, start image recognition

        # Found shape, start OCR

        # If multiple OCR on multiple frames equal, have valid entry / exit

        # Save to database
        # database.insert_new_data("INSERT INTO checkin VALUES(NOW())")
        # If exit key entered, exit


if __name__ == "__main__":
    main()