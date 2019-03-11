import time
import threading
import cv2
from config import current_config as config

class Webcam:
    """Webcam with asynchronous threading support.
    """
    def __init__(self):
        self.cam = cv2.VideoCapture(cv2.CAP_DSHOW)

        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAM_WIDTH)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAM_HEIGHT)
        self.cam.set(cv2.CAP_PROP_BRIGHTNESS, config.CAM_BRIGHTNESS)
        self.cam.set(cv2.CAP_PROP_CONTRAST, config.CAM_CONTRAST)
        self.cam.set(cv2.CAP_PROP_SATURATION, config.CAM_SATURATION)

        _, self.frame = self.cam.read()

        self.running = True
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.lock = threading.Lock()
        self.thread.start()

    def update(self):
        while self.running:
            time.sleep(0.01)
            ok, frame = self.cam.read()
            if not ok:
                raise Exception('Webcam feed broken')
            else:
                with self.lock:
                    self.frame = frame

    def read(self):
        with self.lock:
            frame = self.frame
        return frame

    def release(self):
        self.cam.release()
        self.thread.join()
        return


class VideoClip:
    """Support for simulated run with prerecorded video"""
    def __init__(self, src):
        self.cam = cv2.VideoCapture(src)

    def read(self):
        _, frame = self.cam.read()
        return frame

    def release(self):
        self.cam.release()
        return
