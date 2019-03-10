import numpy as np
import cv2 as cv

cap = cv.VideoCapture(cv.CAP_DSHOW + 1)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1600)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1200)
cap.set(cv.CAP_PROP_BRIGHTNESS, 60)
cap.set(cv.CAP_PROP_CONTRAST, 48)
cap.set(cv.CAP_PROP_SATURATION, 70)

cv.namedWindow('frame', cv.WINDOW_NORMAL)
cv.resizeWindow('frame', 600,300)

# Define codec
fourcc = cv.VideoWriter_fourcc(*'DIVX')
out = cv.VideoWriter('output1.avi',fourcc, 30, (1600,1200), True)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        out.write(frame)
        cv.imshow('frame', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv.destroyAllWindows()
