import time
import serial

from datatypes import Data 
from datatypes import PointType 

class Device:

    COM_CODES = {
        "GET_FIRMWARE": b"\x10",
        "SET_FREQ": b"\x20",
        "READ_DATA": b"\x30",
        "MEASURE_AT_FREQ": "f",
        "CALIBRATE_SI5351_FREQ": b"\x40",
        "STOP_GEN": b"\x50",
    }

    BAUDRATE = 115200

    def __init__(self):
        self.serial_port = serial.Serial()
        self.serial_port.timeout = 2
        self.serial_port.baudrate = self.BAUDRATE
        # freq in Hz
        self.min_freq = 100000
        self.max_freq = 450000000
        self.step_freq = 449900
    
    def connect(self, port):
        print(port)
        self.serial_port.port = port
        self.serial_port.open()
        time.sleep(1)  # wait until mcu is available
        # self.firmware = self.get_firmware()
        # print(self.firmware)

    def disconnect(self):
        self.serial_port.close()

    def is_connected(self):
        return self.serial_port.is_open

    def measure_at_freq(self, freq):
        self.serial_port.write(f'{self.COM_CODES["MEASURE_AT_FREQ"]}{";"}{freq}'.encode())
        data = int(self.serial_port.readline())
        print(data)
        return data

    def clean_buffers(self):
        self.serial_port.reset_input_buffer()
        self.serial_port.reset_output_buffer()

    def acquire_single(self) -> Data:    
        data = Data([], [], PointType.RAW)

        for freq in range(self.min_freq, self.max_freq + self.step_freq, self.step_freq):
            data.frequency.append(freq)
            adc_data = self.measure_at_freq(freq)
            data.points.append(adc_data) 
        return data

    def get_firmware(self):
        ret_val = self.serial_port.write(self.COM_CODES["GET_FIRMWARE"])
        data = self.serial_port.readline()
        return data
    