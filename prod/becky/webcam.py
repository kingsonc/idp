import threading
import cv2
from config import current_config as config

class Webcam:
    """Asynchronous threaded version of webcam. Aim to provide higher fps"""
    def __init__(self):
        self.cam = cv2.VideoCapture(cv2.CAP_DSHOW + 1)

        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAM_WIDTH)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAM_HEIGHT)
        self.cam.set(cv2.CAP_PROP_BRIGHTNESS, config.CAM_BRIGHTNESS)
        self.cam.set(cv2.CAP_PROP_CONTRAST, config.CAM_CONTRAST)
        self.cam.set(cv2.CAP_PROP_SATURATION, config.CAM_SATURATION)

        _, self.frame = self.cam.read()

        self.thread = threading.Thread(target=self.update, daemon=True)
        self.lock = threading.Lock()
        self.thread.start()

    def update(self):
        while True:
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


# class Webcam:
#     def __init__(self):
#         self.cam = cv2.VideoCapture(cv2.CAP_DSHOW + 1)

#         self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAM_WIDTH)
#         self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAM_HEIGHT)
#         self.cam.set(cv2.CAP_PROP_BRIGHTNESS, config.CAM_BRIGHTNESS)
#         self.cam.set(cv2.CAP_PROP_CONTRAST, config.CAM_CONTRAST)
#         self.cam.set(cv2.CAP_PROP_SATURATION, config.CAM_SATURATION)

        # _, frame = self.cam.read()


#     def read(self):
#         ok, frame = self.cam.read()

#         if not ok:
#             raise Exception('Webcam feed broken')
#         else:
#             return frame

#     def release(self):
#         self.cam.release()
#         return
