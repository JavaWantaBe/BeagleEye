__author__ = 'richard'

##
#   @file capmanager.py
#
#   @brief Capture manager is a multithreaded object that populates a queue with image frames
#
#

import logging

cap_log = logging.getLogger('capture')

from threading import Thread, Condition
import time
import Queue

try:                    # In a try catch because module does not come with default libraries
    import cv2
except ImportError:
    cap_log.exception("Could not import cv2")


__all__ = ['CaptureManager']


class CaptureManager(Thread):
    """ CaptureManager used for continuous flow of I/O from device """
    def __init__(self, device, queue_size=10, fps=10):
        Thread.__init__(self)  # Initialize parent
        # Private Variables
        self._device = cv2.VideoCapture(device)
        self._queue = Queue.Queue(queue_size)
        #self._width = self._device.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
        #self._height = self._device.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
        self._fps = 0
        self._desired_fps = fps
        self._state = Condition()
        self._paused = True

        cap_log.debug("Capture Manager instance created")

    def run(self):
        self.resume()  # unpause self
        while True:
            with self._state:
                if self._paused:
                    self._state.wait()  # block until notified

            s_time = time.time()
            successful_capture, image = self._device.read()

            if successful_capture:
                try:
                    self._queue.put(image)
                except Queue.Full:
                    pass
                cv2.waitKey(1000 / self._desired_fps)
                self._fps = 1 / (time.time() - s_time)
            else:
                cap_log.error("Could not capture from device")

    def pause(self):
        with self._state:
            self._paused = True  # make self block and wait

    def resume(self):
        with self._state:
            self._paused = False
            self._state.notify()  # unblock self if waiting

    def get_size(self):
        return self._queue.qsize()

    def get_image(self):
        img = 0
        try:
            img = self._queue.get()
        except Queue.Empty:
            cap_log.exception("Could not retrieve image")
        finally:
            return img

    @property
    def get_fps(self):
        return self._fps

    @property
    def get_dimensions(self):
        return self._height, self._height

    def set_dimensions(self, height, width):
        self._device.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
        self._device.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)

    @property
    def get_queue(self):
        return self._queue

    def purge_queue(self):
        """
        Function to purge the queue if needed.  This could happen if long delays happen on other
        threads and the queue is filled with stale images
        """
        while not self._queue.empty():
            try:
                tmp = self._queue.get()
            except Queue.Empty:
                cap_log.exception("Queue Empty")


def test_cap():

    cap = CaptureManager(0, 10, 10)
    cap.start()
    print "Going into while loop"

    while True:
        print "Happy: " + str(cap.get_fps)
        cv2.imshow("Debugger", cap.get_image())
        cv2.waitKey(10)


if __name__ == "__main__":
    test_cap()