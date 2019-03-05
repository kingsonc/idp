import cv2
import numpy as np

import becky.comms as comms
import becky.fuelcell as fuelcell
import becky.motor as motor
import becky.path_finder as path_finder
import becky.plotter as plotter
import becky.robot as robot
import becky.webcam as webcam
import becky.vision as vision

if __name__ == '__main__':
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output.avi',fourcc, 10.0, (2946,1473))

    cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Camera', 1200,600)

    ### Uncomment one of below to choose between live webcam or recorded video
    # camera = webcam.Webcam()
    camera = webcam.VideoClip('../test_files/output1.avi')

    becky = robot.RobotState()
    fctracker = fuelcell.FuelCellsTracker()
    navigation = path_finder.PathFinder()
    navigation.process.start()
    arduino = comms.ArduinoNC('COM15')

    path = None

    while True:
        timer = cv2.getTickCount()

        frame = camera.read()
        frame = vision.cam2map_transform(frame)
        fuelcell_coords = vision.find_fuel_cells(frame)
        fuelcells = fctracker.update(fuelcell_coords)
        # Update tracker based on new fuelcell positions
        visible_fuelcells = fctracker.visible_fuelcells()
        robot_coords = becky.find_robot(frame)
        # Generate simulation table
        table_plot = plotter.board_plot(becky, visible_fuelcells)

        if robot_coords:
            # Passing variables for path finding
            try:
                # Clear multiprocessing queues
                navigation.visible_fuelcells_q.get_nowait()
                navigation.robot_coords_q.get_nowait()
                navigation.target_coords_q.get_nowait()
            except:
                pass
            finally:
                try:
                    # Push new values into queues
                    navigation.visible_fuelcells_q.put_nowait(visible_fuelcells)
                    navigation.robot_coords_q.put_nowait(robot_coords)
                    navigation.target_coords_q.put_nowait((150,50))
                except:
                    pass

        # Get new path if available
        try:
            path = navigation.path_q.get_nowait()
        except:
            pass

        # Calculate motor speeds based on path
        if path:
            ML, MR, path_pos, target_coords = motor.PIDController(becky, path)
            table_plot = path_finder.plot_path(table_plot,path, path_pos, target_coords)

            arduino.motor_L.speed = ML
            arduino.motor_R.speed = MR

        overall = np.hstack((table_plot,frame))
        cv2.imshow('Camera', overall)
        # out.write(overall)

        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        print(f"FPS: {fps}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            # navigation.process.terminate()
            # navigation.process.join()
            # arduino.running = False
            # camera.running = False
            break
