__author__ = 'trey'

import logging
import cv2
import numpy as np
import Tkinter
from capmanager import CaptureManager
import direction

# Initialize logger for presentation
presentlog = logging.getLogger('presentation')

# Initialize capture manager, must start later though
capture = CaptureManager(0, 100)

def show_project():

    capture.start()
    my_queue = capture.get_queue
    orig_queue = capture.get_queue
    image, detected = direction.direction_detected(my_queue)
    while True:
        image, detected = direction.direction_detected(my_queue)
        root = Tkinter.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        cv2.namedWindow("Original", cv2.WINDOW_FREERATIO)
        cv2.resizeWindow("Original", screen_width/2, (screen_height/2)-55)  # top
        cv2.imshow("Original", orig_queue.get())
        cv2.moveWindow("Original", screen_width/2, 0)
        if detected:
            cv2.putText(image, 'Motion Detected!!', (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255),2,cv2.LINE_AA)
            cv2.resizeWindow("Differential Image", screen_width/2, (screen_height/2)-30)  # bottom
            cv2.imshow("Differential Image", image)
            cv2.moveWindow("Differential Image", screen_width/2, screen_height/2)
            cv2.waitKey(1000)
            detected = 0

if __name__ == "__main__":
    show_project()
