# -*- coding: utf-8 -*-
__author__ = 'trey'


import logging
import cv2
import numpy as np
import time
from sys import exit

#from matplotlib import pyplot as plt

# Initialize video capture and logger
directlog = logging.getLogger('direction')


# Holds average of image set
timed_average = []
bin_size = 128
deltaMeanThreshold = 0.2


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
    np.reshape(bins, bin_size, 1)     # Creates a new array of 256 1D arrays with 1 number each

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


def find_average(image_queue):
    global timed_average
    
    count = 0
    temp = []
    hist_value = []
    
    # TODO: Takes set of frames and averages histograms

    while not image_queue.empty() or count < 10:
        # Get an image from the queue
        image = image_queue.get()
        show_histogram(image)

        # Calculate histogram for the image
        hist_value.append(cv2.calcHist(image, [0], None, [bin_size], [0, 255]))
        count += 1

    # Once the hist_value array is filled with 10 histograms
    # Add all 10 histograms together
    # hist_value contains 10 arrays, each of those arrays are an array with bin(n) arrays
    # TODO: Need to have an array of arrays to make this work
    for x in xrange(count):
        temp[:] += hist_value[x]
    print "Added"

    # Divide values in temp array to get timed average
    # timed_average[:] = temp / count

def direction_detected(frame):
    global timed_average
    # TODO: Detect direction of change
    # We need to figure out that difference in values we want to determine
    # whether or not we are detecting direction of change.
    return False

def test_unit():
    image = cv2.imread("images/aseal.jpg")
    cv2.imshow("Test", image)
    #bgr = show_histogram(image)
    hist = cv2.calcHist(image, [0], None, [bin_size], [0,255])
    d_hist = np.empty_like(hist)
    d_hist[:] = hist * 2

    print("\n-------------------- Histogram Values ---------------------\n")
    print(hist)
    print("\n-------------------- Doubled Histogram Values ---------------------\n")
    print(d_hist)

    cv2.waitKey(10000)



#      TRYING TO LOOP 10 TIMES FOR DIRECTION DETECTION
#
#
def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    
    return cv2.bitwise_and(d1, d2)

def w_show_histogram(frame, doShow):

    
    hist_height = 64
    hist_width = 256
    bin_width = hist_width/bin_size

    #Create an empty image for the histogram
    h = np.zeros((hist_height,hist_width))
    
    # CREATE EMPTY ARRAY FOR BINS
    bins = np.arange(bin_size, dtype=np.int32).reshape(bin_size, 1)

    # BUILDS A HISTOGRAM AND NORMALIZE
    hist_item = cv2.calcHist([frame], [0], None, [bin_size], [0, 255])
    cv2.normalize(hist_item, hist_item, 0, 255, cv2.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    pts = np.column_stack((bins,hist))

    #Loop through each bin and plot the rectangle in white
    for x,y in enumerate(hist):
        cv2.rectangle(h,(x*bin_width,y),(x*bin_width + bin_width-1,hist_height),(255),-1)

    #Flip upside down
    h=np.flipud(h)

    #Show the histogram
    if doShow:
        cv2.imshow('colorhist',h)

 #   plt.hist(hist_item.ravel(),256,[0,256])
 #   plt.title('Histogram for gray scale picture')
 #   plt.show()

    cv2.waitKey(10)
    return hist_item

def w_find_direction(image_queue, size):
    count = 0
    trend = 0
    widthBuffer = 0
    runningMean = 0
    runningMeanSum = 0

    #time.sleep(3)
    print size

    # GET FIRST THREE FRAMES FOR MOTION DETECTION
    #prevFrame = cv2.cvtColor(image_queue.get(), cv2.COLOR_RGB2GRAY)
    currentFrame = cv2.cvtColor(image_queue.get(), cv2.COLOR_RGB2GRAY)
    nextFrame = cv2.cvtColor(image_queue.get(), cv2.COLOR_RGB2GRAY)

    #prevFrame = cv2.GaussianBlur(prevFrame,(3,3),0) 
    #currentFrame = cv2.GaussianBlur(currentFrame,(3,3),0) 
    #nextFrame = cv2.GaussianBlur(nextFrame,(3,3),0) 

    #prevHistogram = w_show_histogram(prevFrame, False)
    #currentHistogram = w_show_histogram(currentFrame, False)
    #nextHistogram = w_show_histogram(nextFrame, False)
    
    for count in range(9):

        # CHECK FOR DIFFERENCE
        #delta = diffImg(prevHistogram, currentHistogram, nextHistogram)
        #delta = diffImg(prevFrame, currentFrame, nextFrame)

        delta = cv2.absdiff(currentFrame, nextFrame)
        w_show_histogram(delta, True)
        # THRESHOLD AND DETECT MOVEMENT
        #ret, th1 = cv2.threshold(delta, 0, 255, cv2.THRESH_BINARY_INV)

        deltaMean, deltaStdDev = cv2.meanStdDev(delta)

        # CALCULATE A RUNNING MEAN
        if count != 0:
            runningMeanSum += deltaMean
            runningMean = runningMeanSum / count

            print "                   ", deltaMean, " : runMean: ", runningMean
                
            # IF THE CURRENT DELTA JUMPS OVER 20% OF THE CURRENT RUNNING AVERAGE
            # DETECT AS MOVEMENT.
            if (deltaMean / runningMean) >= (1 + deltaMeanThreshold):
                print "RISING MOVEMENT!"
            elif (deltaMean / runningMean) <= (1 - deltaMeanThreshold):
                print "FALLING MOVEMENT"

        # SET UP FOR NEXT CYCLE
        #prevFrame = currentFrame
        currentFrame = nextFrame
        nextFrame = cv2.cvtColor(image_queue.get(), cv2.COLOR_RGB2GRAY)

        #prevFrame = cv2.GaussianBlur(prevFrame,(3,3),0) 
        #currentFrame = cv2.GaussianBlur(currentFrame,(3,3),0) 
        #nextFrame = cv2.GaussianBlur(nextFrame,(3,3),0) 
        
        #prevHistogram = w_show_histogram(prevFrame, False)
        #currentHistogram = w_show_histogram(currentFrame, False)
        #nextHistogram = w_show_histogram(nextFrame, False)


        #cv2.imshow('delta', delta)


    k = cv2.waitKey(30) & 0xff
    #if k == 27:
    #    exit()
'''
    firstFrame = cv2.cvtColor(image_queue.get(), cv2.COLOR_RGB2GRAY)
    secondFrame = cv2.cvtColor(image_queue.get(), cv2.COLOR_RGB2GRAY)
    thirdFrame = cv2.cvtColor(image_queue.get(), cv2.COLOR_RGB2GRAY)
    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyWindow(winName)
        exit()

'''
if __name__ == "__main__":
    test_unit()