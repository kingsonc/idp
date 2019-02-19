"""
Usage: cell_finder_video.py
.
Test script to find coordinates of fuel cells in video.
"""

import numpy as np
import cv2

# Open sample video
cap = cv2.VideoCapture('test_files/table3_sample.wmv')

# Create output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output2.avi',fourcc, 20.0, (2946,1473))

cv2.namedWindow('feed', cv2.WINDOW_NORMAL)
cv2.resizeWindow('feed', 1200,600)

# For writing coordinate text overlay
font = cv2.FONT_HERSHEY_SIMPLEX

def print_map_coords(cx, cy):
    """ Converts image coordinates into table coordinates in cm
    """
    x_cm = round(cx*240/1473, 2)
    y_cm = round((1473-cy)*240/1473, 2)

    return 'X:' + str(x_cm) + ', Y:' + str(y_cm)

while(cap.isOpened()):
    ret, frame = cap.read()

    # Perspective transform. See perspective_transform.py
    dst = frame[:,55:1528]
    dst = cv2.copyMakeBorder(dst,199,74,0,0,cv2.BORDER_CONSTANT, value=[0,0,0])
    pts1 = np.float32([[1417,1393],[1466,606],[10,495],[4,999]])
    pts2 = np.float32([[1425,1395],[1473,604],[0,482],[0,977]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(dst,M,(1473,1473))

    # Rotate image clockwise 90 deg
    rows, cols, channels = dst.shape
    rotation_M = cv2.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),-90,1)
    dst = cv2.warpAffine(dst,rotation_M,(cols,rows))

    # Gaussian blur to remove noise
    dst = cv2.GaussianBlur(dst,(5,5),0)

    # Convert to HSV colourspace for colour thresholding
    hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)

    # # Upper and lower HSV bounds
    lower_thresh = np.array([95, 100, 100])
    upper_thresh = np.array([110, 255, 255])

    # Obtain mask of fiters
    mask = cv2.inRange(hsv, lower_thresh, upper_thresh)

    # Apply mask to original image
    masked = cv2.bitwise_and(dst, dst, mask=mask)

    # Convert frame to grayscale and find object contours
    gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Overlay contours onto image
    cv2.drawContours(masked, contours, -1, (0,255,0), 3)

    # Calculate centre of mass for each contour found
    for contour in contours:
        M = cv2.moments(contour)
        area = cv2.contourArea(contour)

        if area < 100:
            continue

        # Sometimes m00 is zero (?)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            # Draw crosshair in centre of contours
            cv2.line(masked, (cx-15, cy-15), (cx+15, cy+15), (0,0,255), 5)
            cv2.line(masked, (cx-15, cy+15), (cx+15, cy-15), (0,0,255), 5)

            # Overlay coordinates text
            cv2.putText(masked, print_map_coords(cx,cy), (cx-120,cy+50), \
                        font, 1, (100,0,255),2,cv2.LINE_AA)

    # Combine original and masked w/ contours frames
    overall = np.hstack((masked,dst))
    cv2.imshow('feed', overall)

    # Write output to disk
    out.write(overall)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()