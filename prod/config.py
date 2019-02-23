# CONFIGURATION FILE FOR BEQCUERELLA

import numpy as np

class Config:
    """Generic values applicable to all tables"""
    CAM_WIDTH = 1600
    CAM_HEIGHT = 1200

    FRAME_POST_PROCESS_SHAPE = (1473,1473)

    TABLE_SIZE = (240,240)

    # Fuel cell tracking
    BLUE_LOWER_THRESH = np.array([85, 60, 100])
    BLUE_UPPER_THRESH = np.array([120, 255, 255])

    # Robot tracking
    GREEN_LOWER_THRESH = np.array([60, 100, 100])
    GREEN_UPPER_THRESH = np.array([95, 255, 255])

    MAP_COORDS = np.float32([[1425,1395],[1473,604],[0,482],[0,977]])


class Table3Config(Config):
    """Specific values only applicable to table 3"""
    TABLE = 3

    CAM_BRIGHTNESS = 60
    CAM_CONTRAST = 48
    CAM_SATURATION = 70

    # Perspective transformation
    CAMERA_COORDS = np.float32([[1417,1393],[1466,606],[10,495],[4,999]])

    # Trim to only display table area
    TABLE_EDGE_TOP = 55
    TABLE_EDGE_BOT = 1528

    # Padding to cover missing area not visible in camera
    TABLE_BORDER_FILL_LEFT = 74
    TABLE_BORDER_FILL_RIGHT = 199


class Table2Config(Config):
    """Specific values only applicable to table 3"""
    CAM_BRIGHTNESS = 60
    CAM_CONTRAST = 48
    CAM_SATURATION = 70

    # Perspective transformation
    CAMERA_COORDS = np.float32([[1417,1393],[1466,606],[10,495],[4,999]])

    # Trim to only display table area
    TABLE_EDGE_TOP = 55
    TABLE_EDGE_BOT = 1528

    # Padding to cover missing area not visible in camera
    TABLE_BORDER_FILL_LEFT = 74
    TABLE_BORDER_FILL_RIGHT = 199

current_config = Table3Config()
