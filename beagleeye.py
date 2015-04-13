__author__ = 'richard'

import cv2
import database
import logging
from os import path
import direction
import icu
import ocr
from settings import SettingManager
import sys
from threading import Thread
from Queue import Queue



# *********************Web Video ************************
#   The video file mjpg/video.mjpg is simply being accessed
#   on a http server (this is a live feed)
http_video_file = "http://myapplecam.com/mjpg/video.mjpg"

# **********************Local Video *********************
#   OpenCV can also read some saved video files but
#   it'll take some work installing the codecs
local_video_file = ""

# *********************Settings Mangaer******************
#   Settings manager
local_settings = SettingManager()

# ******************** Video Device *********************
#   Capture device used
capture_device = 0
capture_queue = Queue(100)

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
def setup_capture_device(device):
    global capture_device  # Accesses the global previously defined

    if device == capture_device:
        cam_settings = local_settings.get_settings('camera')

        capture_device = cv2.VideoCapture(int(cam_settings['device']))

        # Setup device
        capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, int(cam_settings['width']))
        capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, int(cam_settings['height']))
        capture_device.set(cv2.CAP_PROP_FPS, int(cam_settings['fps']))
    else:
        capture_device = cv2.VideoCapture(device)

    # Print current device settings
    syslog.debug('width: {}, height: {},\
    fps: {}'.format(str(capture_device.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    str(capture_device.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                    str(capture_device.get(cv2.CAP_PROP_FPS))))



##
#   @brief Gets image from capture device
#
#   Retrieves a single frame from the configured capture device
#
#   @returns - frame
def get_frame():
    while not capture_queue.full():
        ret, frame = capture_device.read()

        if ret:
            capture_queue.put(frame)
            cv2.waitKey(100)
        else:
            syslog.error("Failed to capture image")


def print_usage():
    print """Usage: python beagleeye.py [h|l|u]
    h: http video file
    l: local video file
    u: usb or integrated camera device"""


def main():

    argument_length = len(sys.argv)

    if argument_length == 1:
        # no supplied argument is okay -- use default
        video_file_type = ""
    elif argument_length == 2:
        # if there is a supplied argument, make sure there is only one
        video_file_type = sys.argv[1]
    else:
        # otherwise print an error
        print_usage()
        exit(1)

    # Note: in cv2 the VideoCapture function can be used to create feeds from
    #   both a usb device or a file
    capture = ""
    if video_file_type == 'h':
        capture = http_video_file
    elif video_file_type == 'l':
        capture = local_video_file
    elif video_file_type == 'u':
        capture = capture_device
    elif video_file_type == "":
        # no supplied
        capture = capture_device
    else:
        print_usage()
        exit(1)

    setup_capture_device(capture)

    detected_movement = False   # Variable for determining when to exit loop
    on_beaglebone = False

    # Start a separate thread to collect video frames
    video_thread = Thread(name='video_capture', target=get_frame)
    video_thread.start()

    syslog.info("system started")

    while True:
        # Check if coming or going
        while not detected_movement:
            try:
                image = capture_queue.get()

                if not on_beaglebone:
                    cv2.imshow('Debugging Window', image)
                    direction.show_histogram(image)
                    cv2.waitKey(10)

                if direction.direction_detected(image):
                    detected_movement = True
            except Queue.Empty:
                syslog.debug("Queue empty")

        detected_movement = False

        # If check equals setting, start image recognition

        # Found shape, start OCR

        # If multiple OCR on multiple frames equal, have valid entry / exit

        # Save to database
        database.insert_new_data("INSERT INTO checkin VALUES(NOW())")
        # If exit key entered, exit
        myin = raw_input()

        if not on_beaglebone:
            cv2.destroyAllWindows()

        if myin == 'x':
            break


if __name__ == "__main__":
    main()