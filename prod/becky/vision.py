import numpy as np
import cv2
from config import current_config as config

def cam2map_transform(frame):
    """Transforms a camera frame into a table-coordinate accurate image

    Args:
        frame: frame from camera feed in BGR

    Returns:
        frame: transformed table-accurate frame in BGR
    """
    camera_coords = config.CAMERA_COORDS
    map_cords = config.MAP_COORDS

    # Trim frame (remove non-table area) -> Pad frame (simulate missing table
    # area) -> Perspective transform
    frame = frame[:,config.TABLE_EDGE_TOP:config.TABLE_EDGE_BOT]
    frame = cv2.copyMakeBorder(frame, config.TABLE_BORDER_FILL_RIGHT,
                               config.TABLE_BORDER_FILL_LEFT, 0, 0,
                               cv2.BORDER_CONSTANT, value=[0,0,0])
    M = cv2.getPerspectiveTransform(camera_coords,map_cords)
    frame = cv2.warpPerspective(frame, M, config.FRAME_POST_PROCESS_SHAPE)

    # Rotate image clockwise 90 deg
    rows, cols = config.FRAME_POST_PROCESS_SHAPE
    M = cv2.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0), -90, 1)
    frame = cv2.warpAffine(frame, M, config.FRAME_POST_PROCESS_SHAPE)

    # Gaussian blur to remove noise
    frame = cv2.GaussianBlur(frame, (5,5), 0)
    return frame

def find_fuel_cells(frame):
    """Identifies positions of fuel cells.

    Args:
        frame: map-accurate frame in BGR

    Returns:
        fuelcell_coords (list): list of identified fuel cell coordinates
    """
    fuelcell_coords = []
    kernel = np.ones((7,7),np.uint8)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, config.BLUE_LOWER_THRESH, config.BLUE_UPPER_THRESH)
    masked = cv2.bitwise_and(frame, frame, mask=mask)
    gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    cnts, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Only keep the top 10 largest contours
    if len(cnts) > 10:
        cnts = sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True)[:10]

    for cnt in cnts:
        M = cv2.moments(cnt)
        # Add 1e-5 to avoid division by zero
        cx = int(M['m10']/(M['m00'] + 1e-5))
        cy = int(M['m01']/(M['m00'] + 1e-5))

        fuelcell_coords.append((cx,cy))

    return fuelcell_coords

def map_coord_to_cm(coord):
    x = round(coord[0]*config.TABLE_SIZE[0]/config.FRAME_POST_PROCESS_SHAPE[0])
    y = round(coord[1]*config.TABLE_SIZE[1]/config.FRAME_POST_PROCESS_SHAPE[1])
    return (x,y)
