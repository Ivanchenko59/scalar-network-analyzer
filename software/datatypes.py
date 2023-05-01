from dataclasses import dataclass
from enum import Enum
from typing import List

class PointType(Enum):
    RAW = 1
    MVOLTS = 2
    DB = 3

ADC_RESOLUTION = 4095   # 12 bit
VOLTAGE_REF = 3300      # mV

def convert_adc_to_mV(data_adc):
    data_mV = data_adc / ADC_RESOLUTION * VOLTAGE_REF
    return data_mV

def convert_adc_array_to_mV(data_adc_array):
    data_mV_array = []
    for data_adc in data_adc_array:
        data_mV = data_adc / ADC_RESOLUTION * VOLTAGE_REF
        data_mV_array.append(data_mV)
    return data_mV_array

def convert_mV_to_dBm(data_mV):
    slope = 25          # mV / dBm
    intercept = -84      # dBm
    
    data_dBm = data_mV / slope + intercept
    return data_dBm

def convert_mV_array_to_dBm(data_mV_array):
    slope = 25          # mV / dBm
    intercept = -84      # dBm
    
    data_dBm_array = []
    for data_mV in data_mV_array:
        data_dBm = data_mV / slope + intercept
        data_dBm_array.append(data_dBm)
    return data_dBm_array

def convert_adc_array_to_dBm(data_adc):
    return convert_mV_array_to_dBm(convert_adc_array_to_mV(data_adc))


@dataclass
class Data:
    frequency: List[int]
    points: List[float]
    point_type: PointType

    func_map = {
        (PointType.RAW, PointType.MVOLTS): convert_adc_array_to_mV,
        (PointType.RAW, PointType.DB): convert_adc_array_to_dBm
    }

    def convert_to(self, point_type:PointType):
        key = self.point_type, point_type
        convert_type = Data.func_map[key]
        return convert_type(self.points)

    def convert_points_to(points, point_type_from:PointType, point_type_to:PointType):
        key = point_type_from, point_type_to
        convert_type = Data.func_map[key]
        return convert_type(points)