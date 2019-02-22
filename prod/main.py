import cv2
import numpy as np
import matplotlib.pyplot as plt
import becky.fuelcell as fuelcell
import becky.robot as robot
import becky.webcam as webcam
import becky.vision as vision
import becky.plotter2 as plotter

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi',fourcc, 10.0, (2946,1473))

cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Camera', 1200,600)

### Uncomment one of below to choose between live webcam or recorded video
# camera = webcam.Webcam()
camera = webcam.VideoClip('../test_files/output1.avi')

becky = robot.RobotState()
fctracker = fuelcell.FuelCellsTracker()

frame = camera.read()

while True:
    timer = cv2.getTickCount()

    frame = camera.read()
    frame = vision.cam2map_transform(frame)
    fuelcell_coords = vision.find_fuel_cells(frame)
    fuelcells = fctracker.update(fuelcell_coords)

    robot_coords = becky.find_robot(frame)

    # for fc in fuelcells.values():
    #     if fc.visible == True:
    #         cv2.line(frame, (fc.coord[0]-10, fc.coord[1]-10), (fc.coord[0]+10, fc.coord[1]+10), (0,0,255), 5)
    #         cv2.line(frame, (fc.coord[0]-10, fc.coord[1]+10), (fc.coord[0]+10, fc.coord[1]-10), (0,0,255), 5)
    #         cv2.putText(frame, "ID: " + str(fc.FCID), (fc.coord[0],fc.coord[1]-15), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

    # if robot_coords:
    #     cv2.line(frame, (robot_coords[0]-10, robot_coords[1]-10), (robot_coords[0]+10, robot_coords[1]+10), (0,0,255), 5)
    #     cv2.line(frame, (robot_coords[0]-10, robot_coords[1]+10), (robot_coords[0]+10, robot_coords[1]-10), (0,0,255), 5)
    #     robot_coords_cm = vision.map_coord_to_cm(robot_coords)
    # else:
    #     robot_coords_cm = 0

    table_plot = plotter.board_plot(becky, fctracker.visible_fuelcells())
    overall = np.hstack((table_plot,frame))

    cv2.imshow('Camera', overall)
    # out.write(overall)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    print(f"FPS: {fps}")
    print(f"Robot coords: {robot_coords}")

    for fc in fuelcells.values():
        print(fc.__dict__)
