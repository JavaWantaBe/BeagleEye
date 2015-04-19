__author__ = 'richard'

##
#   @file capmanager.py
#
#   @brief Capture manager is a multithreaded object that populates a queue with image frames
#
#

import logging

cap_log = logging.getLogger('capture')

from threading import Thread
import time
import Queue

try:                    # In a try catch because module does not come with default libraries
    import cv2
except ImportError:
    cap_log.exception("Could not import cv2")


__all__ = ['CaptureManager']


class CaptureManager(Thread):
    """ CaptureManager used for continuous flow of I/O from device """
    def __init__(self, device=0, queue_size=100, fps=10):
        Thread.__init__(self)  # Initialize parent
        # Private Variables
        self._paused = True  # start out paused
        self._device = cv2.VideoCapture(device)
        self._queue = Queue.Queue(queue_size)
        self._width = self._device.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
        self._height = self._device.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
        self._fps = 0
        self._desired_fps = fps

        cap_log.debug("Capture Manager instance created")

    def run(self):
        self._paused = False

        while not self._paused:
            s_time = time.time()

            if not self._queue.full():
                successful_capture, image = self._device.read()

                if successful_capture:
                    self._queue.put(image)
                    self._fps = 1 / (time.time() - s_time)
                    time.sleep(1 / self._desired_fps)
                else:
                    cap_log.error("Could not capture from device")
            else:
                time.sleep(1 / self._desired_fps)
        time.sleep(.1)

    def resume(self):
        self._paused = False

    def pause(self):
        self._paused = True         # make self block and wait

    @property
    def get_size(self):
        return self._queue.qsize()

    @property
    def get_image(self):
        try:
            return self._queue.get()
        except Queue.Empty:
            cap_log.exception("Could not retrieve image")

    @property
    def get_fps(self):
        return self._fps

    @property
    def get_dimensions(self):
        return self._height, self._height

    def set_dimensions(self, height, width):
        self._device.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
        self._device.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)

    def purge_queue(self):
        while not self._queue.empty():
            try:
                tmp = self._queue.get()
            except Queue.Empty:
                cap_log.exception("Queue Empty")


def test_cap():

    cap = CaptureManager(0, 10, 10)
    cap.start()
    print "Going into while loop"
    time.sleep(1)

    while True:
        print "Happy: " + str(cap.get_fps)
        cv2.imshow("Debugging", cap.get_image())


if __name__ == "__main__":
    test_cap()