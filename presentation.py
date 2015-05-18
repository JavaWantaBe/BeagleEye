__author__ = 'trey'

import cv2
import multiprocessing
import Tkinter
import direction
import time

movie = "movie.mp4"

def original(width, height, x, y):
    cap = cv2.VideoCapture(movie)
    time.sleep(2.3)
    while True:
        success, img = cap.read()
        if success:
            cv2.namedWindow("Original", cv2.WINDOW_FREERATIO)
            cv2.resizeWindow("Original", width, height)  # top
            cv2.imshow("Original", img)
            cv2.moveWindow("Original", x, y)
            cv2.waitKey(10)
        else:
            cap.release()
            break

def detection(width, height, x, y):
    loop = True
    cap = cv2.VideoCapture(movie)
    cue = multiprocessing.Queue()

    num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    num_frames = int(num_frames)
    print("Number of frames = " + str(num_frames))

    while num_frames:
        success, img = cap.read()
        if success:
            cue.put(img)
        num_frames -= 1

    while loop:
        #new_queue = cue
        image, detected = direction.direction_detected(cue)
        if detected:
            cv2.putText(image, 'Motion Detected!!', (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255),2,cv2.LINE_AA)
            cv2.imshow("Differential Image", image)
            cv2.waitKey(2300)
            detected = 0
            loop = False
            cap.release()
            cv2.destroyWindow("Differential Image")



def show_project():

    root = Tkinter.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    print "Width  = " + str(screen_width)
    print "Height = " + str(screen_height)

    orig_thread = multiprocessing.Process(target=original, args=(screen_width/2, (screen_height/2)-55, 0, 0))
    detect_thread = multiprocessing.Process(target=detection, args=(screen_width/2, (screen_height/2)-55, screen_width/2, 0))
    orig_thread.start()
    detect_thread.start()

if __name__ == "__main__":
    show_project()
