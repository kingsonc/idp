import math
import cv2
import numpy as np
from config import current_config as config

table = np.zeros(config.FRAME_POST_PROCESS_SHAPE + (3,), np.uint8)
table[:] = (128,128,128)

# Horizontal start white line
cv2.rectangle(table, (0,1289), (1473,1301), (255,255,255), -1)

# Start box left
cv2.rectangle(table, (80,1412), (276,1424), (255,255,255), -1)     #Bot
cv2.rectangle(table, (80,1166), (276,1178), (255,255,255), -1)     #Top
cv2.rectangle(table, (80,1178), (92,1412), (255,255,255), -1)      #Left
cv2.rectangle(table, (264,1178), (276,1412), (255,255,255), -1)    #Right
cv2.rectangle(table, (172,994), (184,1473), (255,255,255), -1)     #Vertical

# Start box right
cv2.rectangle(table, (1197,1412), (1393,1424), (255,255,255), -1)  #Bot
cv2.rectangle(table, (1198,1166), (1393,1178), (255,255,255), -1)  #Top
cv2.rectangle(table, (1197,1178), (1209,1412), (255,255,255), -1)  #Left
cv2.rectangle(table, (1381,1178), (1393,1412), (255,255,255), -1)  #Right
cv2.rectangle(table, (1289,994), (1301,1473), (255,255,255), -1)   #Vertical

# Safe zone
cv2.rectangle(table, (601,1338), (872,1350), (0,255,0), -1)        #Top
cv2.rectangle(table, (601,1338), (614,1473), (0,255,0), -1)        #Left
cv2.rectangle(table, (859,1338), (872,1473), (0,255,0), -1)        #Right

# Shelf
cv2.rectangle(table, (615,1418), (859,1473), (0,204,204), -1)

# Red line
cv2.rectangle(table, (0,730), (1473,743), (0,0,200), -1)

# Horizontal check
cv2.rectangle(table, (368,55), (1105,68), (255,255,255), -1)

# Vertical checks
cv2.rectangle(table, (485,0), (497,123), (255,255,255), -1)
cv2.rectangle(table, (607,0), (620,123), (255,255,255), -1)
cv2.rectangle(table, (730,0), (743,123), (255,255,255), -1)
cv2.rectangle(table, (853,0), (865,123), (255,255,255), -1)
cv2.rectangle(table, (976,0), (988,123), (255,255,255), -1)

def board_plot(robotState, fuelcells):
    current_table = table.copy()

    if robotState.visible == True:
        robot_coords = robotState.lastseen_coords()
        cv2.circle(current_table, robot_coords, 20, (0,255,255), -1)

        robot_orientation = robotState.orientation()
        if robot_orientation:
            robot_arrow_end = (int(robot_coords[0]+200*math.cos(robot_orientation)),
                               int(robot_coords[1]+200*math.sin(robot_orientation)))
            cv2.arrowedLine(current_table,robot_coords,robot_arrow_end,(0,255,0),3)

    for fc in fuelcells:
        cv2.circle(current_table, fc.coord, 10, (255,0,0), -1)
        cv2.putText(current_table, str(fc.FCID),
                    (fc.coord[0],fc.coord[1]-15), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0,0,139), 2);

    return current_table
