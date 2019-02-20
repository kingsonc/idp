"""
Usage: robot_tracking.py
.
Test script to track position of robot.
"""

import numpy as np
import cv2

USE_LIVE_CAM = True

if USE_LIVE_CAM:
    cap = cv2.VideoCapture(cv2.CAP_DSHOW + 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
else:
    # Open sample video
    cap = cv2.VideoCapture('test_files/table3_sample.wmv')

cv2.namedWindow('Tracking', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Tracking', 1200,600)

# Create tracker
tracker = cv2.TrackerMOSSE_create() # super fast and full occlusion recovery (less accurate?)
# tracker = cv2.TrackerKCF_create() # slower but more accurate

# Create output video
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output3.avi',fourcc, 20.0, (1600,1200))

# Read first frame
ret, frame = cap.read()

# Manual bounding box selection
bbox = cv2.selectROI('Tracking', frame, False, False)

# Initialise tracker
ret = tracker.init(frame, bbox)

while True:
    ret, frame = cap.read()
    timer = cv2.getTickCount()

    # Update tracker
    ret, bbox = tracker.update(frame)

    if ret:
        # Object found
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0,0,255), 2, 1)
    else :
        # Cannot find object
        cv2.putText(frame, "Track failed", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(frame, "FPS: " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

    cv2.imshow("Tracking", frame)
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
