import cv2
import beqcuerella.robot as robot
import beqcuerella.webcam as webcam
import beqcuerella.vision as vision

### Uncomment one of below to choose between live webcam or recorded video
# camera = webcam.Webcam()
camera = webcam.VideoClip('../test_files/table3_sample.wmv')

beqc = robot.RobotState()

frame = camera.read()
beqc.find_robot(frame)

while True:
    timer = cv2.getTickCount()

    frame = camera.read()
    frame = vision.cam2map_transform(frame)
    fuelcell_coords = vision.find_fuel_cells(frame)
    robot_coords = beqc.update_tracker(frame)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    print(f"FPS: {fps}")
    print(f"Fuel cell coords: {fuelcell_coords}")
    print(f"Robot coords: {robot_coords}")
