import serial
import threading
import time

class Arduino:
    def __init__(self, port):
        self.ser = serial.Serial(port, baudrate=9600, timeout=1)
        while self.ser.in_waiting == 0:
            continue
        line = self.ser.read_until('\r\n')
        print("Data: " + str(line))

        self.send_cmds = ""
        self.wait_send = False
        self.wait_rcv = False

        self.thread = threading.Thread(target=self.update, daemon=True)
        self.send_cmds_lock = threading.Lock()
        self.thread.start()

    def update(self):
        while True:
            if self.wait_rcv:
                if self.ser.in_waiting >0:
                    line = self.ser.read_until('\r\n')
                    print("Data: " + str(line))
                    self.wait_rcv = False
            elif self.wait_send:
                with self.send_cmds_lock:
                    self.send_cmds += "."
                    print("Sending: " + str(self.send_cmds.encode()))
                    self.ser.write(self.send_cmds.encode())
                    self.send_cmds = ""
                    self.wait_rcv = True
                    self.wait_send = False
            else:
                time.sleep(0.01)

    def send(self, motor_L, motor_R):
        if motor_L.updated:
            with self.send_cmds_lock:
                self.send_cmds += (motor_L.precmd + motor_L.direction
                                   + str(motor_L.speed).zfill(3) + ',')
            motor_L.updated = False
            self.wait_send = True

        if motor_R.updated:
            with self.send_cmds_lock:
                self.send_cmds += (motor_R.precmd + motor_R.direction
                                   + str(motor_R.speed).zfill(3) + ',')
            motor_R.updated = False
            self.wait_send = True

    def release(self):
        self.ser.close()
        self.thread.join()
        return


class ArduinoNC:
    def __init__(self, port):
        self.send_cmds = ""
        self.wait_send = False
        self.wait_rcv = False

        self.thread = threading.Thread(target=self.update, daemon=True)
        self.send_cmds_lock = threading.Lock()
        self.thread.start()

    def update(self):
        while True:
            if self.wait_rcv:
                    self.wait_rcv = False
            elif self.wait_send:
                    self.send_cmds += "."
                    print("Sending: " + str(self.send_cmds.encode()))
                    self.send_cmds = ""
                    self.wait_rcv = True
                    self.wait_send = False
            time.sleep(1)

    def send(self, motor_L, motor_R):
        if motor_L.updated:
            with self.send_cmds_lock:
                self.send_cmds += (motor_L.precmd + motor_L.direction
                                   + str(motor_L.speed).zfill(3) + ',')
            motor_L.updated = False
            self.wait_send = True

        if motor_R.updated:
            with self.send_cmds_lock:
                self.send_cmds += (motor_R.precmd + motor_R.direction
                                   + str(motor_R.speed).zfill(3) + ',')
            motor_R.updated = False
            self.wait_send = True


    def release(self):
        self.thread.join()
        return


# class Arduino:
#     def __init__(self, port):
#         self.ser = serial.Serial(port, baudrate=9600, timeout=1)
#         while self.ser.in_waiting == 0:
#             continue
#         line = self.ser.read_until('\r\n')
#         print("Data: " + str(line))
#         self.ready_to_send = True

#         self.thread = threading.Thread(target=self.update)
#         self.lock = threading.Lock()
#         self.thread.start()

#     def send(self, value):
#         if self.ready_to_send:
#             data = value + '.'
#             print("Sending: " + str(data.encode()))
#             self.ready_to_send = False
#             self.ser.write(data.encode())
#         else:
#             print("Waiting for Arduino")

#     def read(self):
#         if self.ser.in_waiting > 0:
#             line = self.ser.read_until('\r\n')
#             print("Data: " + str(line))
#             self.ready_to_send = True
#         else:
#             print("No data")

#     def close(self):
#         self.ser.close()
