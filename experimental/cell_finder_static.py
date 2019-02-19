"""
Usage: cell_finder_static.py
.
Test script to find coordinates of fuel cells.
"""

import numpy as np
import cv2

img = cv2.imread('test_files/table3_still.jpg', 1)

# Perspective transform. See perspective_transform.py
dst = cv2.resize(img, (1600, 1200), interpolation=cv2.INTER_AREA)
dst = dst[:,55:1528]
dst = cv2.copyMakeBorder(dst,199,74,0,0,cv2.BORDER_CONSTANT, value=[0,0,0])
pts1 = np.float32([[1417,1393],[1466,606],[10,495],[4,999]])
pts2 = np.float32([[1425,1395],[1473,604],[0,482],[0,977]])
M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(dst,M,(1473,1473))

# Gaussian blur to remove noise
dst = cv2.GaussianBlur(dst,(5,5),0)

# Convert to HSV colourspace for colour thresholding
hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)

# Upper and lower HSV bounds
lower_thresh = np.array([95, 102, 192])
upper_thresh = np.array([110, 192, 255])

# Obtain mask of fiters
mask = cv2.inRange(hsv, lower_thresh, upper_thresh)

# Apply mask to original image
final = cv2.bitwise_and(dst, dst, mask=mask)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 600,600)
cv2.imshow('image', final)

cv2.waitKey(0)
cv2.destroyAllWindows()
