import time
import serial
import numpy as np


class Device:

    COM_CODES = {
        "START": b"\x10",
        "GET_FIRMWARE": b"w",
        "CALIBRATE_FREQ": b"\x30",
        "SET_FREQ": b"\x40",
        "STOP_GEN": b"\x50",
        "READ_DATA": b"\x60",
    }
    BUFFER_SIZE = 100  # 512
    BAUDRATE = 115200

    def __init__(self):
        self.serial_port = serial.Serial()
        self.serial_port.baudrate = self.BAUDRATE

    def connect(self, port):
        print(port)
        self.serial_port.port = port
        self.serial_port.open()
        time.sleep(2)  # wait until arduino is available
        self.firmware = self.get_firmware()
        print(self.firmware)

    def disconnect(self):
        self.serial_port.close()

    def write_freq(self):
        self.serial_port.write(self.COM_CODES["SET_FREQ"][self.frequency])

    def clean_buffers(self):
        self.serial_port.reset_input_buffer()
        self.serial_port.reset_output_buffer()

    def acquire_single(self):
        self.serial_port.write(self.COM_CODES["START"])
        data = self.serial_port.read(size=self.BUFFER_SIZE)
        data = np.frombuffer(data, dtype=np.uint8).astype(float) * 5 / 256
        return data

    def get_firmware(self):
        self.serial_port.write(self.COM_CODES["GET_FIRMWARE"])
        data = self.serial_port.readline()
        return data
    
    def is_connected(self):
        return self.serial_port.is_open
