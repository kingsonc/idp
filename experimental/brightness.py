import numpy as np
import cv2


cap = cv2.VideoCapture(cv2.CAP_DSHOW + 1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)

# cap.set(cv2.CAP_PROP_SETTINGS, 1)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 60)
cap.set(cv2.CAP_PROP_CONTRAST, 48)
cap.set(cv2.CAP_PROP_SATURATION, 70)

cv2.namedWindow('test', cv2.WINDOW_NORMAL)
cv2.resizeWindow('test', 1200,600)

while True:
    ret, frame = cap.read()
    cv2.imshow("test", frame)

    # print('brightness: ', cap.get(cv2.CAP_PROP_BRIGHTNESS))
    # print('contrast: ', cap.get(cv2.CAP_PROP_CONTRAST))
    # print('saturation: ', cap.get(cv2.CAP_PROP_SATURATION))

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

cap.release()
