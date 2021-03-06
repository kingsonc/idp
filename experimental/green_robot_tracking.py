"""
Usage: green_robot_tracking.py
.
Test script to track position of robot using green tape.
"""

from collections import deque
import math

import numpy as np
import cv2

# Better list with max length
tracked_pts = deque(maxlen=100)

USE_LIVE_CAM = False

if USE_LIVE_CAM:
    cap = cv2.VideoCapture(cv2.CAP_DSHOW + 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 60)
    cap.set(cv2.CAP_PROP_CONTRAST, 48)
    cap.set(cv2.CAP_PROP_SATURATION, 70)
else:
    # Open sample video
    cap = cv2.VideoCapture('test_files/output5.avi')

cv2.namedWindow('Tracking', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Tracking', 1200,600)

# Create output video
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output4.avi',fourcc, 20.0, (1473,1473))

# GREEN TAPE
lower_thresh = np.array([60, 100, 40])
upper_thresh = np.array([95, 255, 255])

def standard_transform(frame):
    # Coordinates for perspective transform
    camera_pts = np.float32([[1417,1393],[1466,606],[10,495],[4,999]])
    map_pts = np.float32([[1425,1395],[1473,604],[0,482],[0,977]])

    # Perspective transform. See perspective_transform.py
    frame = frame[:,55:1528]
    frame = cv2.copyMakeBorder(frame,199,74,0,0,cv2.BORDER_CONSTANT, value=[0,0,0])
    M = cv2.getPerspectiveTransform(camera_pts,map_pts)
    frame = cv2.warpPerspective(frame,M,(1473,1473))

    # Rotate image clockwise 90 deg
    rows, cols, channels = frame.shape
    rotation_M = cv2.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),-90,1)
    frame = cv2.warpAffine(frame,rotation_M,(cols,rows))

    # Gaussian blur to remove noise
    frame = cv2.GaussianBlur(frame,(7,7),0)

    return frame

# Create tracker
tracker = cv2.TrackerMOSSE_create()

# Read first frame
ret, frame = cap.read()

frame = standard_transform(frame)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_thresh, upper_thresh)
masked = cv2.bitwise_and(frame, frame, mask=mask)
gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

# Find circle in gray masked frame
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 5, param1=50,param2=10,minRadius=20, maxRadius=60)
print(circles)

x_center, y_center, radius = circles[0,0]

# Region of interest bounding box (xmin, ymin, width, height)
bbox = (x_center-(radius+20), y_center-(radius+20), 2*(radius+20), 2*(radius+20))

# Initialise tracker in masked frame
ret = tracker.init(masked, bbox)

while True:
    ret, frame = cap.read()
    timer = cv2.getTickCount()

    frame = standard_transform(frame)

    # Convert to HSV colourspace for colour thresholding
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_thresh, upper_thresh)
    masked = cv2.bitwise_and(frame, frame, mask=mask)

    # Update tracker in masked frame
    ret, bbox = tracker.update(masked)

    if ret:
        # Object found
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1]+  bbox[3]))
        cv2.rectangle(frame, p1, p2, (0,0,255), 2, 1)
        tracked_center = (int(bbox[0]+bbox[2]/2), int(bbox[1]+bbox[3]/2))
        tracked_pts.appendleft(tracked_center)
    else :
        # Cannot find object
        cv2.putText(frame, "Track failed", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    # Draw path of robot
    for i in range(len(tracked_pts)):
        if i == 0:
            continue
        cv2.line(frame, tracked_pts[i-1], tracked_pts[i], (0,0,255), 2)

    # Calculate orientation based on previous position (from 10 frames back)
    if len(tracked_pts) > 10:
        dx = tracked_pts[0][0] - tracked_pts[10][0]
        dy = tracked_pts[0][1] - tracked_pts[10][1]

        # magnitude = math.sqrt(dx**2 + dy**2)
        # dx = int(dx/magnitude)
        # dy = int(dy/magnitude)

        cv2.arrowedLine(frame, tracked_center, (tracked_center[0]+dx, tracked_center[1]+dy), \
                        (255,0,0), 4)

    # Calculate frame rate
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(frame, "FPS: " + str(int(fps)), (100,50), \
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);


    # gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 5, param1=50,param2=10,minRadius=20, maxRadius=60)
    # x_center, y_center, radius = circles[0,0]
    # bbox = (x_center-(radius+20), y_center-(radius+20), 2*(radius+20), 2*(radius+20))
    # p1 = (int(bbox[0]), int(bbox[1]))
    # p2 = (int(bbox[0] + bbox[2]), int(bbox[1]+  bbox[3]))
    # cv2.rectangle(masked, p1, p2, (0,0,255), 2, 1)

    overall = np.hstack((masked,frame))

    cv2.imshow("Tracking", overall)
    # cv2.imshow("Tracking", frame)
    # out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# out.release()
cap.release()
cv2.destroyAllWindows()
