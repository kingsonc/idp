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

        self.motor_L = Motor("L")
        self.motor_R = Motor("R")

        self.wait_send = False
        self.wait_rcv = False

        self.running = True
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.send_cmds_lock = threading.Lock()
        self.thread.start()

    def update(self):
        while self.running:
            if self.wait_rcv:
                if self.ser.in_waiting >0:
                    line = self.ser.read_until('\r\n')
                    print("Data: " + str(line))
                    self.wait_rcv = False
            else:
                send_cmds = self.generate_cmds()
                if send_cmds:
                    send_cmds += "."
                    print("Sending: " + str(send_cmds.encode()))
                    self.ser.write(send_cmds.encode())
                    self.wait_rcv = True
                    self.wait_send = False
                else:
                    time.sleep(0.01)

    def generate_cmds(self):
        cmds = ""
        if self.motor_L.updated:
            cmds += (self.motor_L.precmd + self.motor_L.direction
                     + str(self.motor_L.speed).zfill(3) + ',')
            self.motor_L.updated = False
            self.wait_send = True

        if self.motor_R.updated:
            cmds += (self.motor_R.precmd + self.motor_R.direction
                     + str(self.motor_R.speed).zfill(3) + ',')
            self.motor_R.updated = False
            self.wait_send = True

        return cmds

    def release(self):
        self.ser.close()
        self.thread.join()
        return


class ArduinoNC:
    def __init__(self, port):
        self.motor_L = Motor("L")
        self.motor_R = Motor("R")

        self.wait_send = False
        self.wait_rcv = False

        self.running = True
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.send_cmds_lock = threading.Lock()
        self.thread.start()

    def update(self):
        while self.running:
            if self.wait_rcv:
                self.wait_rcv = False
            else:
                send_cmds = self.generate_cmds()
                if send_cmds:
                    send_cmds += "."
                    print("Sending: " + str(send_cmds.encode()))
                    self.wait_rcv = True
                    self.wait_send = False

            time.sleep(0.01)

    def generate_cmds(self):
        cmds = ""
        if self.motor_L.updated:
            cmds += (self.motor_L.precmd + self.motor_L.direction
                     + str(self.motor_L.speed).zfill(3) + ',')
            self.motor_L.updated = False
            self.wait_send = True

        if self.motor_R.updated:
            cmds += (self.motor_R.precmd + self.motor_R.direction
                     + str(self.motor_R.speed).zfill(3) + ',')
            self.motor_R.updated = False
            self.wait_send = True

        return cmds

    def release(self):
        self.thread.join()
        return


class Motor:
    def __init__(self, side=None):
        self.updated = False
        self._direction = "F"
        self._speed = 0

        if side == 'L':
            self.precmd = "ML"
        elif side == 'R':
            self.precmd = "MR"

    @property
    def direction(self):
        return self._direction

    @property
    def speed(self):
        return self._speed

    @direction.setter
    def direction(self, value):
        if self._direction != value:
            self._direction = value
            self.updated = True

    @speed.setter
    def speed(self, value):
        if self._speed != value:
            self._speed = value
            self.updated = True


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
