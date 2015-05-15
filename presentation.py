__author__ = 'trey'

import logging
import cv2
from threading import Thread
from Queue import Queue
import Tkinter
import direction

# Initialize logger for presentation
presentlog = logging.getLogger('presentation')

# Initialize capture manager, must start later though


def original(source, width, height, x, y):
    cap = cv2.VideoCapture(source)
    while True:
        success, img = cap.read()
        while success:
            cv2.namedWindow("Original", cv2.WINDOW_FREERATIO)
            cv2.resizeWindow("Original", width, (height)-55)  # top
            cv2.imshow("Original", img)
            cv2.moveWindow("Original", x, y)
            cv2.waitKey(10)


def detection(source, width, height, x, y):
    capture = cv2.VideoCapture(source)
    while True:
        success, img = capture.read()



def show_project():

    root = Tkinter.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    print "Width  = " + str(screen_width)
    print "Height = " + str(screen_height)
    original(0, screen_width/2, (screen_height/2)-55, 0, 0)
'''
        if detected:
            cv2.putText(image, 'Motion Detected!!', (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255),2,cv2.LINE_AA)
            cv2.resizeWindow("Differential Image", screen_width/2, (screen_height/2)-30)  # bottom
            cv2.imshow("Differential Image", image)
            cv2.moveWindow("Differential Image", screen_width/2, screen_height/2)
            cv2.waitKey(1000)
            detected = 0
'''
if __name__ == "__main__":
    show_project()
