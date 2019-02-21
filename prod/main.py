import cv2
import beqcuerella.fuelcell as fuelcell
import beqcuerella.robot as robot
import beqcuerella.webcam as webcam
import beqcuerella.vision as vision

### Uncomment one of below to choose between live webcam or recorded video
# camera = webcam.Webcam()
camera = webcam.VideoClip('../test_files/table3_sample.wmv')

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

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    print(f"FPS: {fps}")
    print(f"Fuel cells: {fuelcells}")
    print(f"Robot coords: {robot_coords}")

    for fc in fuelcells.values():
        print(fc.__dict__)
