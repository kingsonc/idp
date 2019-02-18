"""
Usage: perspective_transform.py

Test script to perform 4 point perspective transformation on image. Outputs
non-skewed image to allow navigation control of robot.
"""

import numpy as np
import cv2

# Open test image in colour
img = cv2.imread('test_files/table3_still.jpg', 1)

# Scale image to match video feed resolution
dst = cv2.resize(img, (1600, 1200), interpolation=cv2.INTER_AREA)

# Crop to table area
dst = dst[:,55:1528]

# Pad top and bottom of image to create 1:1 table shape
dst = cv2.copyMakeBorder(dst,199,74,0,0,cv2.BORDER_CONSTANT, value=[0,0,0])

# Coordinates for transformation
# Bottom left corner start box -> bottom right green box
# -> top of rightmost vertical white mesh -> top of leftmost vertical white mesh
pts1 = np.float32([[1417,1393],[1466,606],[10,495],[4,999]])
pts2 = np.float32([[1425,1395],[1473,604],[0,482],[0,977]])

# Find transformation matrix and apply transformation
M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(dst,M,(1473,1473))


# Create window and scale to resonable size
cv2.namedWindow('original', cv2.WINDOW_NORMAL)
cv2.namedWindow('final', cv2.WINDOW_NORMAL)
cv2.resizeWindow('original', 600,600)
cv2.resizeWindow('final', 600,600)

cv2.imshow('original', img)
cv2.imshow('final', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
