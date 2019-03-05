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

    print(robot_pos)
    print(path_idx, path[path_idx])
    print(target_idx, target_coord)

    target_dist_sqr = ((target_coord[0]-robot_pos[0])**2
                       + (target_coord[1]-robot_pos[1])**2)

    if target_dist_sqr == 0:
        print("Already at target")
        return (0, 0, path[path_idx], target_coord)

    # dx dy in map coordinates
    dx = target_coord[0] - robot_pos[0]
    dy = target_coord[1] - robot_pos[1]

    # Transform target to robot coordinates
    x_v = (dx*math.cos(heading) + dy*math.sin(heading))
    y_v = (-dx*math.sin(heading) + dy*math.cos(heading))

    # Desired curvature
    curv = 2*abs(x_v)/target_dist_sqr

    # robot_vec = [math.cos(orientation), math.sin(orientation), 0]
    # heading_vec = [dx,dy,0]

    # if np.cross(robot_vec, heading_vec)[2] > 0:
    if x_v > 0:
        print("turn left")
        ML = int(config.MAX_SPD - curv*config.KP)
        MR = config.MAX_SPD
    else:
        print("turn right")
        ML = config.MAX_SPD
        MR = int(config.MAX_SPD - curv*config.KP)

    if ML < 0:
        MR += abs(ML)*3
        ML = 0
    elif MR < 0:
        ML += abs(MR)*3
        MR = 0

    elif ML < 100:
        MR += (100-ML)*3
        ML = 100
    elif MR < 100:
        ML += (100-ML)*3
        MR = 100

    print("ML:", ML)
    print("MR:", MR)

    return (ML, MR, path[path_idx], target_coord)
