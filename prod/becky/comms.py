import threading
import serial

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
                    print("Sending: " + str(self.send_cmds.encode()))
                    self.ser.write(self.send_cmds.encode())
                    self.wait_rcv = True
                    self.wait_send = False


    def send(self, value):
        with self.send_cmds_lock:
            self.send_cmds = value + '.'
            self.wait_send = True

    def release(self):
        self.ser.close()
        self.thread.join()
        return


class Motor:
    def __init__(self, side=None):
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


class ArduinoNC:
    def __init__(self, port):
        pass

    def update(self):
        pass

    def send(self, value):
        pass

    def release(self):
        pass


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
