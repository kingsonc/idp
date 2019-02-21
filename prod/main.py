import cv2
import beqcuerella.robot as robot
import beqcuerella.webcam as webcam
import beqcuerella.vision as vision

camera = webcam.Webcam()
beqc = robot.RobotState()

frame = camera.read()
beqc.find_robot(frame)

while True:
    timer = cv2.getTickCount()

    frame = camera.read()
    frame = vision.cam2map_transform(frame)
    fuelcell_coords = vision.find_fuel_cells(frame)
    robot_coords = robot.update_tracker(frame)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
