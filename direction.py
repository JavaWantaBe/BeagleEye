__author__ = 'trey'

import logging
import cv2
import numpy as np

# Initialize video capture and logger
directlog = logging.getLogger('direction')

# Holds average of image set
timed_average = []

def show_histogram(frame):
    # Now create a histogram for the frame
    h = np.zeros((300, 256, 3))
    b, g, r = cv2.split(frame)
    bins = np.arange(256).reshape(256, 1)
    color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    for item, col in zip([b, g, r], color):
        hist_item = cv2.calcHist([item], [0], None, [256], [0, 255])
        cv2.normalize(hist_item, hist_item, 0, 255, cv2.NORM_MINMAX)
        hist = np.int32(np.around(hist_item))
        pts = np.column_stack((bins, hist))
        cv2.polylines(h, [pts], False, col)

    h = np.flipud(h)

    # Display histogram
    cv2.imshow('Histogram', h)
    cv2.waitKey(10)


def find_average(image_set):
    global timed_average
    # TODO: Takes set of frames and averages histograms
    print "Complete me"


def direction_detected(frame):
    global timed_average
    # TODO: Detect direction of change
    print "Change is in the air"