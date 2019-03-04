import math

import numpy as np
from scipy.spatial import distance

from config import current_config as config

class Motor:
    def __init__(self, side=None):
        self.updated = False
        self._direction = "F"
        self._speed = 0

        if side == 'L':
            self.precmd = "ML"
        elif side == 'R':
            self.precmd = "MR"

    @property
    def direction(self):
        return self._direction

    @property
    def speed(self):
        return self._speed

    @direction.setter
    def direction(self, value):
        if self._direction != value:
            self._direction = value
            self.updated = True

    @speed.setter
    def speed(self, value):
        if self._speed != value:
            self._speed = value
            self.updated = True


def PIDController(robot_state, path):
    """Calculates turning curvature based on current position and path
    """
    robot_pos = robot_state.lastseen_coords()
    heading = math.pi/2 - robot_state.orientation()
    orientation = robot_state.orientation()
    # Find closest path index
    rel_dist = distance.cdist([robot_pos], path)
    path_idx = rel_dist.argmin()

    # Find look ahead target coordinate
    target_idx = path_idx + config.LOOK_AHEAD
    if target_idx < len(path):
        target_coord = path[target_idx]
    else:
        target_coord = path[-1]

    target_dist_sqr = ((target_coord[0]-robot_pos[0])**2
                       + (target_coord[1]-robot_pos[1])**2)

    # dx dy in map coordinates
    dx = target_coord[0] - robot_pos[0]
    dy = target_coord[1] - robot_pos[1]

    # Transform target to robot coordinates
    x_v = (dx*math.cos(heading) + dy*math.sin(heading))
    y_v = (-dx*math.sin(heading) + dy*math.cos(heading))

    # Desired curvature
    curv = 2*abs(x_v)/target_dist_sqr

    robot_vec = [math.cos(orientation), math.sin(orientation), 0]
    heading_vec = [dx,dy,0]

    if np.cross(robot_vec, heading_vec)[2] > 0:
        ML = int(255-curv*config.KP)
        MR = 255
    else:
        ML = 255
        MR = int(255-curv*config.KP)

    print("ML:", ML)
    print("MR:", MR)

    return (ML, MR)
