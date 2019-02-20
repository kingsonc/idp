import numpy as np
import cv2

def empty_callback(e):
    pass

cv2.namedWindow('feed', cv2.WINDOW_NORMAL)

cv2.namedWindow('filtered', cv2.WINDOW_NORMAL)
cv2.resizeWindow('filtered', 600,300)

cv2.createTrackbar('H_min','feed',0,179,empty_callback)
cv2.createTrackbar('H_max','feed',0,179,empty_callback)
cv2.createTrackbar('S_min','feed',0,255,empty_callback)
cv2.createTrackbar('S_max','feed',0,255,empty_callback)
cv2.createTrackbar('V_min','feed',0,255,empty_callback)
cv2.createTrackbar('V_max','feed',0,255,empty_callback)

USE_LIVE_CAM = False

if USE_LIVE_CAM:
    cap = cv2.VideoCapture(cv2.CAP_DSHOW + 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
else:
    # Open sample video
    cap = cv2.VideoCapture('test_files/table3_sample.wmv')
    frame_counter = 0

while(True):
    ret, frame = cap.read()

    if not USE_LIVE_CAM:
        frame_counter += 1
        print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(frame_counter)
        if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT) - 10:
            frame_counter = 0
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    h_min = cv2.getTrackbarPos('H_min','feed')
    h_max = cv2.getTrackbarPos('H_max','feed')
    s_min = cv2.getTrackbarPos('S_min','feed')
    s_max = cv2.getTrackbarPos('S_max','feed')
    v_min = cv2.getTrackbarPos('V_min','feed')
    v_max = cv2.getTrackbarPos('V_max','feed')

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_thresh = np.array([h_min, s_min, v_min])
    upper_thresh = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(hsv, lower_thresh, upper_thresh)
    final = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('feed', np.zeros((10,10,3), np.uint8))
    cv2.imshow('filtered', final)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
