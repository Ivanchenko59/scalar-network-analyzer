import time
import serial
import numpy as np


class Device:

    COM_CODES = {
        "START": b"r",
        "GET_FIRMWARE": b"w",
        "CALIBRATE_FREQ": b"\x30",
        "SET_FREQ": b"f",
        "STOP_GEN": b"\x50",
        "READ_DATA": b"\x60",
    }
    BUFFER_SIZE = 100  # 512
    BAUDRATE = 115200

    def __init__(self):
        self.serial_port = serial.Serial()
        # self.serial_port.timeout = 1
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
        # self.serial_port.write(f'{self.COM_CODES["SET_FREQ"]} {"1000"}'.encode())  # add freq data
        data = self.serial_port.readline()
        # print(int(data.rstrip('\0')))

    def clean_buffers(self):
        self.serial_port.reset_input_buffer()
        self.serial_port.reset_output_buffer()

    def acquire_single(self):
        x_ret = []
        y_ret = []
        # self.serial_port.write(f'{self.COM_CODES["START"]}'.encode())
        # data = self.serial_port.readline()
        # print(int(data.rstrip('\0')))
        low_freq = 100
        high_freq = 1000
        step = 10

        for freq in range(low_freq, high_freq, step):
            x_ret.append(freq)
            adc_data = self.get_firmware()
            y_ret.append(int(adc_data))
        
        return x_ret, y_ret


    def get_firmware(self):
        ret_val = self.serial_port.write(self.COM_CODES["GET_FIRMWARE"])
        data = self.serial_port.readline()
        return data
    
    def is_connected(self):
        return self.serial_port.is_open
