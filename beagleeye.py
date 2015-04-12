__author__ = 'richard'

import cv2
import database
import logging
from os import path
import direction
import icu
import ocr
import settings

# *********************Settings Mangaer*****************
local_settings = settings.SettingManager()

# ******************** Video Device *********************
capture_device = 0

# ********************** Logger **************************
# Create logger
logging.basicConfig(level=logging.DEBUG,
                    format=('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'),
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
def setup_capture_device():
    global capture_device
    cam_settings = local_settings.get_settings('camera')
    print cam_settings
    capture_device = cv2.VideoCapture(int(cam_settings['device']))
    capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, int(cam_settings['width']))
    capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, int(cam_settings['height']))
    capture_device.set(cv2.CAP_PROP_FPS, int(cam_settings['fps']))


##
#   @brief Gets image from capture device
#
#   Retrieves a single frame from the configured capture device
#
#   @returns - frame
def get_frame():
    ret, frame = capture_device.read()

    if ret:
        return frame
    else:
        syslog.error("Failed to capture image")

def main():
    setup_capture_device()
    syslog.info("system started")

    # *********************** MySQL *************************
    dbParam = local_settings.get_settings('database')

    try:
        db = database.Database(**dbParam)
    except:
        pass
    finally:
        syslog.error("Could not connect to database")

    detected_movement = False   # Variable for determining when to exit loop
    on_beaglebone = False

    while 1:

        # Check if coming or going
        while not detected_movement:
            # Acquire Image
            frame = get_frame()

            if not on_beaglebone:
                cv2.imshow('Debug Output', frame)
                cv2.waitKey(10)
            # if direction.detect(frame):
            #    detected_movement = True

        # If check equals setting, start image recognition

        # Found shape, start OCR

        # If multiple OCR on multiple frames equal, have valid entry / exit

        # Save to database

        # If exit key entered, exit
        myin = raw_input()

        if myin == 'x':
            break


if __name__ == "__main__":
    main()