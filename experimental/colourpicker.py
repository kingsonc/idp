import numpy as np
import cv2 as cv

def empty_callback(e):
    pass

cv.namedWindow('feed')

cv.createTrackbar('H_min','feed',0,179,empty_callback)
cv.createTrackbar('H_max','feed',0,179,empty_callback)
cv.createTrackbar('S_min','feed',0,255,empty_callback)
cv.createTrackbar('S_max','feed',0,255,empty_callback)
cv.createTrackbar('V_min','feed',0,255,empty_callback)
cv.createTrackbar('V_max','feed',0,255,empty_callback)

cap = cv.VideoCapture(0)

while(True):
    ret, frame = cap.read()

    h_min = cv.getTrackbarPos('H_min','feed')
    h_max = cv.getTrackbarPos('H_max','feed')
    s_min = cv.getTrackbarPos('S_min','feed')
    s_max = cv.getTrackbarPos('S_max','feed')
    v_min = cv.getTrackbarPos('V_min','feed')
    v_max = cv.getTrackbarPos('V_max','feed')

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    lower_thresh = np.array([h_min, s_min, v_min])
    upper_thresh = np.array([h_max, s_max, v_max])

    mask = cv.inRange(hsv, lower_thresh, upper_thresh)
    final = cv.bitwise_and(frame, frame, mask=mask)

    cv.imshow('feed', frame)
    cv.imshow('filtered', final)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
