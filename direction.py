__author__ = 'trey'

import logging
import cv2
import numpy as np
import time

# Initialize video capture and logger
cap = cv2.VideoCapture(0)
directlog = logging.getLogger('direction')


while(True):
	# Capture frame by frame
	ret, frame = cap.read()

	# Display image
	cv2.imshow('Super Cool Webcam', frame )
	directlog.info("Webcam displayed.")

	# Now create a histogram for the frame
	h    = np.zeros((300, 256, 3 ))
	b, g, r  = cv2.split(frame)
	bins     = np.arange(256).reshape(256, 1)
	color    = [ (255, 0, 0), (0, 255, 0), (0, 0, 255) ]
	
	for item, col in zip([b, g, r], color ):
		hist_item = cv2.calcHist([item], [0], None, [256], [0,255])
		cv2.normalize( hist_item, hist_item, 0, 255, cv2.NORM_MINMAX)
		hist = np.int32(np.around(hist_item))
		pts = np.column_stack((bins, hist))
		cv2.polylines(h, [pts], False, col)

	h = np.flipud(h)

	# Display histogram
	cv2.imshow('Histogram', h )
	directlog.info("Histogram displayed.")
	
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

