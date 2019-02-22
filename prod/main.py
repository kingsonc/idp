import cv2
import beqcuerella.fuelcell as fuelcell
import beqcuerella.robot as robot
import beqcuerella.webcam as webcam
import beqcuerella.vision as vision

cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Camera', 600,600)

### Uncomment one of below to choose between live webcam or recorded video
camera = webcam.Webcam()
# camera = webcam.VideoClip('../test_files/output5.avi')

beqc = robot.RobotState()
fctracker = fuelcell.FuelCellsTracker()

frame = camera.read()
beqc.find_robot(frame)

while True:
    timer = cv2.getTickCount()

    frame = camera.read()
    frame = vision.cam2map_transform(frame)
    fuelcell_coords = vision.find_fuel_cells(frame)
    fuelcells = fctracker.update(fuelcell_coords)

    robot_coords = beqc.update_tracker(frame)

    for fc in fuelcells.values():
        if fc.visible == True:
            cv2.line(frame, (fc.coord[0]-10, fc.coord[1]-10), (fc.coord[0]+10, fc.coord[1]+10), (0,0,255), 5)
            cv2.line(frame, (fc.coord[0]-10, fc.coord[1]+10), (fc.coord[0]+10, fc.coord[1]-10), (0,0,255), 5)
            cv2.putText(frame, "ID: " + str(fc.FCID), (fc.coord[0],fc.coord[1]-15), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

    if robot_coords:
            cv2.line(frame, (robot_coords[0]-10, robot_coords[1]-10), (robot_coords[0]+10, robot_coords[1]+10), (0,0,255), 5)
            cv2.line(frame, (robot_coords[0]-10, robot_coords[1]+10), (robot_coords[0]+10, robot_coords[1]-10), (0,0,255), 5)

    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    print(f"FPS: {fps}")
    print(f"Fuel cells: {fuelcells}")
    print(f"Robot coords: {robot_coords}")

    for fc in fuelcells.values():
        print(fc.__dict__)
