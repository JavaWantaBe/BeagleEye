__author__ = 'trey'

import logging
import cv2
import numpy as np

# Initialize video capture and logger
directlog = logging.getLogger('direction')

# Holds average of image set
timed_average = []
bin_size = 128

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


def find_average(image_queue):
    global timed_average
    count = 0
    temp = []
    hist_value = []
    # TODO: Takes set of frames and averages histograms

    while not image_queue.empty() or count < 10:
        # Get an image from the queue
        image = image_queue.get()

        # Calculate histogram for the image
        hist_value.append(cv2.calcHist(image, [0], None, [bin_size], [0, 255]))
        count += 1

    # Once the hist_value array is filled with 10 histograms
    # Add all 10 histograms together
    for x in xrange(count):
        temp[:] += hist_value[x]

    # Divide values in temp array to get timed average
    # timed_average[:] = temp / count


def direction_detected(frame):
    global timed_average
    # TODO: Detect direction of change
    return False