import math
import cv2
from config import current_config as config

class RobotState():
    def __init__(self):
        self.tracked_pts = deque(maxlen=500)
        self.tracker = cv2.TrackerMOSSE_create()
        self.tracking = False

    def find_robot(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, config.GREEN_LOWER_THRESH, config.GREEN_UPPER_THRESH)
        masked = cv2.bitwise_and(frame, frame, mask=mask)
        gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 10,
                                   param1=50,param2=10,minRadius=15,maxRadius=40)

        if circles[0,0]:
            x_center, y_center, radius = circles[0,0]
            print(f"Begin tracking. Robot found at ({x_center}, {y_center}).")
            # Region of interest bounding box (xmin, ymin, width, height)
            bbox = (x_center-(radius+20), y_center-(radius+20), 2*(radius+20), 2*(radius+20))

            ret = self.tracker.init(masked, bbox)
            self.tracking = True if ret else False
            self.tracked_pts.appendleft((x_center, y_center))
            return (x_center, y_center)
        else:
            print("Robot not found.")
            return 0

    def update_tracker(self, frame):
        if not self.tracking:
            print("Robot not being tracked. Searching for robot.")
            self.find_robot(frame)
            return

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, config.GREEN_LOWER_THRESH, config.GREEN_UPPER_THRESH)
        masked = cv2.bitwise_and(frame, frame, mask=mask)

        ret, bbox = self.tracker.update(masked)
        if ret:
            tracked_center = (int(bbox[0]+bbox[2]/2), int(bbox[1]+bbox[3]/2))
            self.tracked_pts.appendleft(tracked_center)
            print(f"Robot tracked. At {tracked_center}.")
            return tracked_center
        else :
            print("Robot tracking failed. Searching for robot.")
            self.tracking = False
            self.find_robot(frame)
            return

    def lastseen_coords(self):
        if self.tracked_pts:
            return self.tracked_pts[0]
        else:
            return (0,0)

    def orientation(self):
        if len(tracked_pts) < 10:
            print("Insufficient data to determine robot orientation.")
            return None

        dx = tracked_pts[0][0] - tracked_pts[10][0]
        dy = tracked_pts[0][1] - tracked_pts[10][1]

        return math.atan2(dy,dx)
