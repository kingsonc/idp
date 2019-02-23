import numpy as np
import cv2
from config import current_config as config

def table3():
    # Left limit
    pts = np.array([[[0,0],[104,0],[70,1472],[0,1472]]])
    cv2.fillPoly(default_grid,pts,(255,255,255))

    # Right limit
    cv2.rectangle(default_grid, (1283,0), (1472,1472), (255,255,255), -1)

    # Lighting
    cv2.rectangle(default_grid, (1154,984), (1282,1472), (255,255,255), -1)

default_grid = np.zeros(config.FRAME_POST_PROCESS_SHAPE+(3,), dtype=np.uint8)
if config.TABLE == 3:
    table3()

def generate_grid(visible_fuelcells):
    grid = default_grid.copy()
    for fuelcell in visible_fuelcells:
        if not fuelcell.target:
            cv2.circle(grid, fuelcell.coord, 101, (255,255,255), -1)
    return grid
