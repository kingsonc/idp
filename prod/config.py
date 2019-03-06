# CONFIGURATION FILE FOR BEQCUERELLA

import numpy as np

class Config:
    """Generic values applicable to all tables"""
    CAM_WIDTH = 1600
    CAM_HEIGHT = 1200

    FRAME_POST_PROCESS_SHAPE = (1473,1473)

    TABLE_SIZE = (240,240)

    # Fuel cell tracking
    BLUE_LOWER_THRESH = np.array([90, 70, 130])
    BLUE_UPPER_THRESH = np.array([120, 255, 255])

    # Robot tracking
    GREEN_LOWER_THRESH = np.array([60, 100, 120])
    GREEN_UPPER_THRESH = np.array([90, 255, 255])

    MAP_COORDS = np.float32([[1425,1395],[1473,604],[0,482],[0,977]])

    # PID Controller
    LOOK_AHEAD = 30
    KP = 2000
    MIN_SPD = 40
    MAX_SPD = 80

    # INITIAL_PATH = [(200, 10), (199, 10), (198, 10), (197, 10), (196, 10), (195, 10), (194, 10), (193, 10), (192, 10), (191, 10), (190, 10), (189, 10), (188, 10), (187, 10), (186, 10), (185, 10), (184, 10), (183, 10), (182, 10), (181, 10), (180, 10), (179, 10), (178, 10), (177, 10), (176, 10), (175, 10), (174, 10), (173, 10), (172, 10), (171, 10), (170, 10), (169, 10), (168, 10), (167, 10), (166, 10), (165, 10), (164, 10), (163, 10), (162, 10), (161, 10), (160, 10), (159, 10), (158, 10), (157, 10), (156, 10), (155, 10), (154, 10), (153, 10), (152, 10), (151, 10), (150, 10), (149, 10), (148, 10), (147, 10), (146, 10), (145, 10), (144, 10), (143, 10), (142, 10), (141, 10), (140, 10), (139, 10), (138, 10), (137, 10), (136, 10), (135, 10), (134, 10), (133, 10), (132, 10), (131, 10), (130, 10), (129, 10), (128, 10), (127, 10), (126, 10), (125, 10), (124, 10), (123, 10), (122, 10), (121, 10), (120, 10), (119, 10), (118, 10), (117, 10), (116, 10), (115, 10), (114, 10), (113, 10), (112, 10), (111, 10), (110, 10), (109, 10), (108, 10), (107, 10), (106, 10), (105, 10), (104, 10), (103, 10), (102, 10), (101, 10), (100, 10), (99, 10), (98, 10), (97, 10), (96, 10), (95, 10), (94, 10), (93, 10), (92, 10), (91, 10), (90, 10), (89, 10), (88, 10), (87, 10), (86, 10), (85, 10), (84, 10), (83, 10), (82, 10), (81, 10), (80, 10), (79, 10), (78, 10), (77, 10), (76, 10), (75, 10), (74, 10), (73, 10), (72, 10), (71, 10), (70, 10), (69, 10), (68, 10), (67, 10), (66, 10), (65, 10), (64, 10), (63, 10), (62, 10), (61, 10), (60, 10), (60, 11), (60, 12), (60, 13), (59, 14), (58, 15), (57, 16), (56, 17), (55, 18), (54, 19), (53, 20), (52, 21), (51, 22), (50, 23), (49, 24), (48, 25), (47, 26), (46, 27), (45, 28), (44, 29), (43, 30), (42, 31), (41, 32), (40, 33), (39, 34), (38, 35), (37, 36), (36, 37), (35, 38), (34, 39), (33, 40), (33, 41), (33, 42), (33, 43), (33, 44), (32, 45), (31, 46), (30, 47), (30, 48), (30, 49), (30, 50), (30, 51), (30, 52), (30, 53), (30, 54), (30, 55), (30, 56), (30, 57), (30, 58), (30, 59), (30, 60), (30, 61), (30, 62), (30, 63), (30, 64), (30, 65), (30, 66), (30, 67), (30, 68), (30, 69), (30, 70), (30, 71), (30, 72), (30, 73), (30, 74), (30, 75), (30, 76), (30, 77), (30, 78), (30, 79), (30, 80), (30, 81), (30, 82), (30, 83), (30, 84), (30, 85), (30, 86), (30, 87), (30, 88), (30, 89), (30, 90), (30, 91), (30, 92), (30, 93), (30, 94), (30, 95), (30, 96), (30, 97), (30, 98), (30, 99), (30, 100), (30, 101), (30, 102), (30, 103), (30, 104), (30, 105), (30, 106), (30, 107), (30, 108), (30, 109), (30, 110), (30, 111), (30, 112), (30, 113), (30, 114), (30, 115), (30, 116), (30, 117), (30, 118), (30, 119), (30, 120), (30, 121), (30, 122), (30, 123), (30, 124), (30, 125), (30, 126), (30, 127), (30, 128), (30, 129), (30, 130), (30, 131), (30, 132), (30, 133), (30, 134), (30, 135), (30, 136), (30, 137), (30, 138), (30, 139), (30, 140), (30, 141), (30, 142), (30, 143), (30, 144), (30, 145), (30, 146), (30, 147), (30, 148), (30, 149), (30, 150), (30, 151), (30, 152), (30, 153), (30, 154), (30, 155), (30, 156), (30, 157), (30, 158), (30, 159), (30, 160), (30, 161), (30, 162), (30, 163), (30, 164), (30, 165), (30, 166), (30, 167), (30, 168), (30, 169), (30, 170), (30, 171), (30, 172), (30, 173), (30, 174), (30, 175), (30, 176), (30, 177), (30, 178), (30, 179), (30, 180), (30, 181), (30, 182), (30, 183), (30, 184), (30, 185), (30, 186), (30, 187), (30, 188), (30, 189), (30, 190), (30, 191), (30, 192), (30, 193), (30, 194), (30, 195), (30, 196), (30, 197), (30, 198), (30, 199), (30, 200), (30,201), (30,202), (30,203), (30,204), (30,205), (30,206), (30,207), (30,208), (30,209), (30,210), ]
    INITIAL_PATH = [(200, 17), (199, 17), (198, 17), (197, 17), (196, 17), (195, 17), (194, 17), (193, 17), (192, 17), (191, 17), (190, 17), (189, 17), (188, 17), (187, 17), (186, 17), (185, 17), (184, 17), (183, 17), (182, 17), (181, 17), (180, 17), (179, 17), (178, 17), (177, 17), (176, 17), (175, 17), (174, 17), (173, 17), (172, 17), (171, 17), (170, 17), (169, 17), (168, 17), (167, 17), (166, 17), (165, 17), (164, 17), (163, 17), (162, 17), (161, 17), (160, 17), (159, 17), (158, 17), (157, 17), (156, 17), (155, 17), (154, 17), (153, 17), (152, 17), (151, 17), (150, 17), (149, 17), (148, 17), (147, 17), (146, 17), (145, 17), (144, 17), (143, 17), (142, 17), (141, 17), (140, 17), (139, 17), (138, 17), (137, 17), (136, 17), (135, 17), (134, 17), (133, 17), (132, 17), (131, 17), (130, 17), (129, 17), (128, 17), (127, 17), (126, 17), (125, 17), (124, 17), (123, 17), (122, 17), (121, 17), (120, 17), (119, 17), (118, 17), (117, 17), (116, 17), (115, 17), (114, 17), (113, 17), (112, 17), (111, 17), (110, 17), (109, 17), (108, 17), (107, 17), (106, 17), (105, 17), (104, 17), (103, 17), (102, 17), (101, 17), (100, 17), (99, 17), (98, 17), (97, 17), (96, 17), (95, 17), (94, 17), (93, 17), (92, 17), (91, 17), (90, 17), (89, 17), (88, 17), (87, 17), (86, 17), (85, 17), (84, 17), (83, 17), (82, 17), (81, 17), (80, 17), (79, 17), (78, 17), (77, 17), (76, 17), (75, 17), (74, 17), (73, 17), (72, 17), (71, 17), (70, 17), (69, 17), (68, 17), (67, 17), (66, 17), (65, 17), (64, 17), (63, 17), (62, 17), (61, 17), (60, 17), (60, 17), (60, 17), (60, 17), (59, 17), (58, 17), (57, 17), (56, 17), (55, 18), (54, 19), (53, 17), (52, 21), (51, 22), (50, 23), (49, 24), (48, 25), (47, 26), (46, 27), (45, 28), (44, 29), (43, 30), (42, 31), (41, 32), (40, 33), (39, 34), (38, 35), (37, 36), (36, 37), (35, 38), (35, 39), (35, 40), (35, 41), (35, 42), (35, 43), (35, 44), (35, 45), (35, 46), (35, 47), (35, 48), (35, 49), (35, 50), (35, 51), (35, 52), (35, 53), (35, 54), (35, 55), (35, 56), (35, 57), (35, 58), (35, 59), (35, 60), (35, 61), (35, 62), (35, 63), (35, 64), (35, 65), (35, 66), (35, 67), (35, 68), (35, 69), (35, 70), (35, 71), (35, 72), (35, 73), (35, 74), (35, 75), (35, 76), (35, 77), (35, 78), (35, 79), (35, 80), (35, 81), (35, 82), (35, 83), (35, 84), (35, 85), (35, 86), (35, 87), (35, 88), (35, 89), (35, 90), (35, 91), (35, 92), (35, 93), (35, 94), (35, 95), (35, 96), (35, 97), (35, 98), (35, 99), (35, 100), (35, 101), (35, 102), (35, 103), (35, 104), (35, 105), (35, 106), (35, 107), (35, 108), (35, 109), (35, 110), (35, 111), (35, 112), (35, 113), (35, 114), (35, 115), (35, 116), (35, 117), (35, 118), (35, 119), (35, 120), (35, 121), (35, 122), (35, 123), (35, 124), (35, 125), (35, 126), (35, 127), (35, 128), (35, 129), (35, 130), (35, 131), (35, 132), (35, 133), (35, 134), (35, 135), (35, 136), (35, 137), (35, 138), (35, 139), (35, 140), (35, 141), (35, 142), (35, 143), (35, 144), (35, 145), (35, 146), (35, 147), (35, 148), (35, 149), (35, 150), (35, 151), (35, 152), (35, 153), (35, 154), (35, 155), (35, 156), (35, 157), (35, 158), (35, 159), (35, 160), (35, 161), (35, 162), (35, 163), (35, 164), (35, 165), (35, 166), (35, 167), (35, 168), (35, 169), (35, 170), (35, 171), (35, 172), (35, 173), (35, 174), (35, 175), (35, 176), (35, 177), (35, 178), (35, 179), (35, 180), (35, 181), (35, 182), (35, 183), (35, 184), (35, 185), (35, 186), (35, 187), (35, 188), (35, 189), (35, 190), (35, 191), (35, 192), (35, 193), (35, 194), (35, 195), (35, 196), (35, 197), (35, 198), (35, 199), (35, 200), (35,201), (35,202), (35,203), (35,204), (35,205), (35,206), (35,207), (35,208), (35,209), (35,210), ]


class Table3Config(Config):
    """Specific values only applicable to table 3"""
    TABLE = 3

    CAM_BRIGHTNESS = 50
    CAM_CONTRAST = 50
    CAM_SATURATION = 80

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
