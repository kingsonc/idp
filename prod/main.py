import math

import cv2
import numpy as np

import becky.comms as comms
# import becky.fuelcell as fuelcell
import becky.motor_controller as motor_controller
import becky.path_finder as path_finder
import becky.plotter as plotter
import becky.robot as robot
import becky.webcam as webcam
import becky.vision as vision
from config import current_config as config

if __name__ == '__main__':
    ## Save output video
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output.avi',fourcc, 10.0, (2946,1473))

    cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Camera', 1200,600)

    ### Uncomment one of below to choose between live webcam or recorded video ###
    camera = webcam.Webcam()
    # camera = webcam.VideoClip('../test_files/output1.avi')

    # Initialise objects and threads
    becky = robot.RobotState()
    # fctracker = fuelcell.FuelCellsTracker()
    # navigation = path_finder.PathFinder()
    # navigation.process.start()
    arduino = comms.Arduino('COM15')

    path = None
    path_override = False
    reversing = False

    while True:
        timer = cv2.getTickCount()

        frame = camera.read()
        frame = vision.cam2map_transform(frame)
        # fuelcell_coords = vision.find_fuel_cells(frame)
        # fuelcells = fctracker.update(fuelcell_coords)
        ## Update tracker based on new fuelcell positions
        # visible_fuelcells = fctracker.visible_fuelcells()
        visible_fuelcells = []
        robot_coords = becky.find_robot(frame)
        # Generate simulation table
        table_plot = plotter.board_plot(becky, visible_fuelcells)

        # Choose current path
        if becky.state == "INITIAL":
            path = config.INITIAL_PATH
            # path = config.TEST_PATH
            path_override = True
        elif becky.state == "GO_TO_MIDDLE":
            path = config.GO_MIDDLE_PATH
            path_override = True
        elif becky.state == "REVERSE":
            if not reversing:
                # Initial set up on first change to reversing
                reversing = True
                arduino.start_reverse()
                becky.tracked_pts.clear()
                becky.tracked_pts_cm.clear()
                path = config.REVERSE_PATH
                path_override = True
        # else:
        #     try:
        #         # Clear multiprocessing queues
        #         navigation.visible_fuelcells_q.get_nowait()
        #         navigation.robot_coords_q.get_nowait()
        #         navigation.target_coords_q.get_nowait()
        #     except:
        #         pass

        #     try:
        #         # Push new values into queues
        #         visible_fuelcells = []
        #         navigation.visible_fuelcells_q.put_nowait(visible_fuelcells)
        #         # navigation.robot_coords_q.put_nowait(robot_coords)
        #         navigation.robot_coords_q.put_nowait((60,10))
        #         navigation.target_coords_q.put_nowait((200,10))
        #     except:
        #         pass

        # if not path_override:
        #     # Get new path if available
        #     try:
        #         path = navigation.path_q.get_nowait()
        #     except:
        #         pass

        if path and robot_coords:
            # Calculate motor speeds based on path
            ML, MR, turn_cmd, new_orientation, path_pos, target_coords, at_target = motor_controller.PIDController(becky, path)
            table_plot = path_finder.plot_path(table_plot, path, path_pos, target_coords)

            # Move to next state when current path is complete
            if at_target:
                at_target = False
                if becky.state == "INITIAL":
                    becky.state = "GO_TO_MIDDLE"
                elif becky.state == "GO_TO_MIDDLE":
                    becky.state = "REVERSE"
                    # 180 degree turn to orientate for reversing
                    arduino.turn_cmd = "MTL7800,"
                    new_orientation = math.pi/2
                elif becky.state == "REVERSE":
                    pass

            if reversing:
                ML, MR = MR, ML

            # Reset robot turning state when Arduino reports turning complete
            if not arduino.turning and becky.turning:
                becky.turning = False
                becky.tracked_pts.clear()
                becky.tracked_pts_cm.clear()

            if turn_cmd and not arduino.turning:
                # Send turning command to Arduino if not already turning
                arduino.turning = True
                arduino.turn_cmd = turn_cmd
                becky.turn(new_orientation)
                print("Sharp turn")
                turn_cmd = None
            else:
                # Send new speeds to Arduino
                arduino.motor_L.speed = ML
                arduino.motor_R.speed = MR

        # Combine table simulation and actual camera input
        overall = np.hstack((table_plot,frame))
        cv2.imshow('Camera', overall)
        # out.write(overall)        ## Uncomment to save output to video

        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        print(f"FPS: {fps}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            # navigation.process.terminate()
            # navigation.process.join()
            # arduino.running = False
            # camera.running = False
            break
