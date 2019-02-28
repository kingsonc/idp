import sys
import cv2
import numpy as np

import becky.comms as comms
import becky.fuelcell as fuelcell
import becky.path_finder as path_finder
import becky.plotter2 as plotter
import becky.robot as robot
import becky.webcam as webcam
import becky.vision as vision

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi',fourcc, 10.0, (2946,1473))

cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Camera', 1200,600)

cv2.namedWindow('grid', cv2.WINDOW_NORMAL)
cv2.resizeWindow('grid', 600,600)

### Uncomment one of below to choose between live webcam or recorded video
# camera = webcam.Webcam()
camera = webcam.VideoClip('../test_files/output1.avi')

becky = robot.RobotState()
fctracker = fuelcell.FuelCellsTracker()
arduino = comms.Arduino('COM15')

motor_L = comms.Motor("L")
motor_R = comms.Motor("R")

while True:
    timer = cv2.getTickCount()

    frame = camera.read()
    frame = vision.cam2map_transform(frame)
    fuelcell_coords = vision.find_fuel_cells(frame)
    fuelcells = fctracker.update(fuelcell_coords)
    visible_fuelcells = fctracker.visible_fuelcells()

    robot_coords = becky.find_robot(frame)

    grid = path_finder.generate_grid(visible_fuelcells)

    if robot_coords:
        if robot_coords[1] < 737:
            motor_L.speed = 255
            motor_R.speed = 0
            # arduino.send('MLF255,MRF000,')
        else:
            motor_L.speed = 0
            motor_R.speed = 255
            # arduino.send('MLF000,MRF255,')

    arduino.send(motor_L, motor_R)

    table_plot = plotter.board_plot(becky, visible_fuelcells)
    overall = np.hstack((table_plot,frame))

    cv2.imshow('grid', grid)
    cv2.imshow('Camera', overall)
    # out.write(overall)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    print(f"FPS: {fps}")
    # print(f"Robot coords: {robot_coords}")

    # for fc in fuelcells.values():
    #     print(fc.__dict__)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        sys.exit()
        # arduino.release()
        # camera.release()
        break
