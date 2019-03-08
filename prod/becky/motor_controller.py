import math

import numpy as np
from scipy.spatial import distance

from config import current_config as config

def PIDController(robot_state, path):
    """Calculates turning curvature based on current position and path
    """
    robot_pos = robot_state.lastseen_coords_cm()
    heading = (robot_state.orientation()+(7/2)*math.pi) % (2*math.pi)
    orientation = robot_state.orientation()
    # Find closest path index
    rel_dist = distance.cdist([robot_pos], path)
    path_idx = rel_dist.argmin()

    # Find look ahead target coordinate
    target_idx = path_idx - config.LOOK_AHEAD
    if target_idx < len(path) and target_idx >= 0:
        target_coord = path[target_idx]
    else:
        target_coord = path[-1]
        return (0, 0, 0, 0, path[path_idx], target_coord)

    target_dist_sqr = ((target_coord[0]-robot_pos[0])**2
                       + (target_coord[1]-robot_pos[1])**2)

    if target_dist_sqr < 10:
        print("Already at target")
        return (0, 0, 0, 0, path[path_idx], target_coord)

    # dx dy in map coordinates
    dx = target_coord[0] - robot_pos[0]
    dy = target_coord[1] - robot_pos[1]

    # Transform target to robot coordinates
    x_v = (dx*math.cos(heading) + dy*math.sin(heading))
    y_v = (-dx*math.sin(heading) + dy*math.cos(heading))

    # Desired curvature
    curv = 2*abs(x_v)/target_dist_sqr

    if x_v > 0:
        print("turn left")
        ML = int(config.MAX_SPD - curv*config.KP)
        MR = config.MAX_SPD
    else:
        print("turn right")
        ML = config.MAX_SPD
        MR = int(config.MAX_SPD - curv*config.KP)

    turn_cmd = None
    new_orientation = None
    # Extreme sharp turns
    if ML < config.MIN_SPD or MR < config.MIN_SPD:
        angle_diff = math.degrees((math.atan2(y_v,x_v)+(7/2)*math.pi) % (2*math.pi))
        if angle_diff > 180:
            angle_diff = 360-angle_diff

        if ML < config.MIN_SPD:
            turn_duration = int(angle_diff*43.5)
            turn_cmd = "MTL" + str(turn_duration).zfill(4) + ','
            ML = 0
            MR = 0
        elif MR < config.MIN_SPD:
            turn_duration = int(angle_diff*43.5)
            turn_cmd = "MTR" + str(turn_duration).zfill(4) + ','
            ML = 0
            MR = 0

        new_orientation = math.atan2(dy,dx)

    print("ML:", ML)
    print("MR:", MR)

    return (ML, MR, turn_cmd, new_orientation, path[path_idx], target_coord)
