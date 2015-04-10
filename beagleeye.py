__author__ = 'richard'

import cv2
import database
import logging
import os


# *********************  Globals *************************
db_connected = False

# ********************** Logger **************************
# Create logger
logging.basicConfig(level=logging.DEBUG,
                    format=('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'),
                    datefmt='%m-%d %H:%M',
                    filename=os.curdir + os.sep + 'log' + os.sep + 'system.log',
                    filemode='a')
# Setup file handler
fh = logging.FileHandler('./log/system.log')
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

# ******************** Video Device *********************
cap = cv2.VideoCapture(0)


# *********************** MySQL *************************
dbParam = {'host': 'localhost', 'user': 'beagle', 'password': '123foo', 'database': 'beagleeye'}
try:
    db = database.Database(dbParam)
except:
    pass
finally:
    syslog.error("Could not connect to database")

# logger.info("Database connection is:" + db_connected)

# Load settings

syslog.info("system started")

while 1:
    # Acquire Image
    ret, frame = cap.read()

	# Check if coming or going

	# If check equals setting, start image recognition

	# Found shape, start OCR

	# If multiple OCR on multiple frames equal, have valid entry / exit

	# Save to database

	# If exit key entered, exit
    myin = raw_input()
    if myin == 'x':
        break