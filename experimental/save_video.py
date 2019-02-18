import numpy as np
import cv2 as cv

cap = cv.VideoCapture(cv.CAP_DSHOW + 1)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1600)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1200)

# Define codec
fourcc = cv.VideoWriter_fourcc(*'DIVX')
out = cv.VideoWriter('output.avi',fourcc, 30.0, (1600,1200), True)

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
