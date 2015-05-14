# -*- coding: utf-8 -*-
__author__ = 'trey'


import logging
import cv2
import numpy as np
from capmanager import CaptureManager


# Initialize video capture and logger
directlog = logging.getLogger('direction')


# Holds average of image set
timed_average = []
bin_size = 128

def diffImg(t0,t1,t2):
    # Run differentials
    d1 = cv2.absdiff(t0,t1)
    d2 = cv2.absdiff(t1,t2)

    return cv2.bitwise_and(d1,d2)

def show_histogram(frame):
    # Create a histogram for the frame
    h = np.zeros((300, bin_size, 3))  # Creates an array 300 rows x 256 columns with 3 values in each array
    b, g, r = cv2.split(frame)   # Splits image into respective b, g, r arrays
    """ Setup our bins which are how many divisions we are going to separate the number of colors
      into.  This is the unit of measure on the X axis of a histogram.  The Y axis is used to represent
      intensity of that color.  To do this we need the X axis to be n bins wide.  So if we where
      to divide our colors into 24 units we would need an array consisting of 24 single dimension arrays.
      The following lines create that structure by first creating a single dimension array with how many
      bins we are going to use.  The next function reshape, is used to transform that array into
      the same number we used in the creation of the array, into that number of separate arrays."""
    bins = np.arange(0, bin_size, 1)  # Creates an array that starts at 0 to 255 and increments by 1
    np.reshape(bins, bin_size, 1)     # Creates a new array of bin_size 1D arrays with 1 number each

    color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    # The zip function creates a permutation that consists of a combination of both arguments

    for item, col in zip([b, g, r], color):
        """
        cv2.calcHist(images, channels, mask, histSize, ranges[, hist[, accumulate]])
        1.  images : it is the source image of type uint8 or float32. it should be given in square brackets, ie, [img].
        2.  channels : it is also given in square brackets. It the index of channel for which we calculate histogram.
            For example, if input is grayscale image, its value is [0]. For color image, you can pass [0],[1] or [2] to
            calculate histogram of blue,green or red channel respectively.
        3.  mask : mask image. To find histogram of full image, it is given as “None”. But if you want to find
            histogram of particular region of image, you have to create a mask image for that and give it as mask.
        4.  histSize : this represents our BIN count. Need to be given in square brackets. For full scale, we pass
            [256].
        5.  ranges : this is our RANGE. Normally, it is [0,256].
        """
        hist_item = cv2.calcHist([item], [0], None, [bin_size], [0, 255])
        """
        The function normalizes the histogram bins by scaling them so that the sum of the bins becomes equal to
            factor.
        1.  src – input array.
        2.  dst – output array of the same size as src .
        3.  alpha – norm value to normalize to or the lower range boundary in case of the range normalization.
        4.  beta – upper range boundary in case of the range normalization; it is not used for the norm normalization.
        5.  normType – normalization type (see the details below).
        6.  dtype – when negative, the output array has the same type as src; otherwise, it has the same number of
            channels as src and the depth =CV_MAT_DEPTH(dtype).
        7.  mask – optional operation mask.
        """
        cv2.normalize(hist_item, hist_item, 0, 255, cv2.NORM_MINMAX)

        hist = np.int32(np.around(hist_item))

        pts = np.column_stack((bins, hist))

        cv2.polylines(h, [pts], False, col)

    h = np.flipud(h)

    # Display histogram
    cv2.imshow('Histogram', h)
    cv2.waitKey(10)
    return b, g, r

def direction_detected(image_queue):
    global counter, max_count
    counter = 0
    max_count = 0
    # TODO: Detect direction of change
    t_minus = cv2.cvtColor(image_queue.get(), cv2.COLOR_RGB2GRAY)
    t = cv2.cvtColor(image_queue.get(), cv2.COLOR_RGB2GRAY)
    t_plus = cv2.cvtColor(image_queue.get(), cv2.COLOR_RGB2GRAY)

    while True:
        diff = diffImg(t_minus, t, t_plus)
        cv2.normalize(diff, diff, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
        cv2.namedWindow("Differential Image", cv2.WINDOW_FREERATIO)
        cv2.imshow("Differential Image", diff)
        positive_count = (diff > 180).sum()
        if positive_count > max_count:
            counter += 1
            if counter == 4:
                counter = 0
                directlog.debug("Motion Detected")
                return diff, 1
            max_count = positive_count
        else:
            max_count = 0
            counter = 0

        # Read next image
        t_minus = t
        t = t_plus
        t_plus = cv2.cvtColor(image_queue.get(), cv2.COLOR_RGB2GRAY)

def test_unit():
    global timed_average
    capture = CaptureManager(0, 100)
    capture.start()
    my_queue = capture.get_queue
    print("Direction detected = ")
    print(direction_detected(my_queue))
    cv2.waitKey(10)

if __name__ == "__main__":
    test_unit()
