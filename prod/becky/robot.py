from collections import deque
import math
import cv2
from config import current_config as config
import becky.vision as vision

class RobotState():
    def __init__(self):
        self.state = "INITIAL"
        self.tracked_pts = deque(maxlen=10)
        self.tracked_pts_cm = deque(maxlen=10)
        self.last_orientation = -math.pi/2      # Starting orientation
        self.turning = False
        self.visible = False

    def find_robot(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, config.GREEN_LOWER_THRESH, config.GREEN_UPPER_THRESH)
        masked = cv2.bitwise_and(frame, frame, mask=mask)
        gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 30,
                                   param1=50,param2=15,minRadius=25,maxRadius=35)

        if circles is None:
            print("Robot not found.")
            self.visible = False
            return 0
        else:
            x_center, y_center, radius = circles[0,0]
            # x_center = int(x_center)
            x_center = int(x_center+(736.5-x_center)/9)
            y_center = int(y_center+(736.5-y_center)/9)
            coords_cm = vision.map_coord_to_cm((x_center,y_center))
            # print(f"Robot found at ({coords_cm}).")
            self.visible = True

            self.tracked_pts.appendleft((x_center, y_center))
            self.tracked_pts_cm.appendleft(coords_cm)
            return coords_cm

    def lastseen_coords(self):
        if self.tracked_pts:
            return self.tracked_pts[0]
        else:
            return (0,0)

    def lastseen_coords_cm(self):
        if self.tracked_pts:
            return self.tracked_pts_cm[0]
        else:
            return (0,0)

    def orientation(self):
        if self.turning:
            return self.last_orientation

        if len(self.tracked_pts) <= 5:
            return self.last_orientation

        dx = self.tracked_pts[0][0] - self.tracked_pts[5][0]
        dy = self.tracked_pts[0][1] - self.tracked_pts[5][1]

        mag = dx**2 + dy**2
        if mag < 250:
            # print("Robot not moving")
            return self.last_orientation

        orientation = math.atan2(dy,dx)
        self.last_orientation = orientation
        return orientation

    def turn(self, new_orientation):
        self.last_orientation = new_orientation
        self.turning = True
