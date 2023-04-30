import numpy as np
import json

FILENAME = "calibration_data.json"

def write_calibration_data(data):
        with open(FILENAME, 'w') as f:
            json.dump(data, f)

def read_calibration_data():
    with open(FILENAME, 'r') as file:
        data = json.load(file)
    return data

def perform_calibration(measurement_data):
    calibration_data = read_calibration_data()
    ampl_cal_interp = np.interp(
        measurement_data['frequency'], 
        calibration_data['frequency'], 
        calibration_data['calib_adc']
    )
    calibrated_data = np.subtract(
        convert_adc_array_to_dBm(measurement_data['raw_adc']), 
        convert_adc_array_to_dBm(ampl_cal_interp)
        )
    return measurement_data['frequency'], calibrated_data


def convert_adc_to_mV(data_adc):
    data_mV = data_adc / 4095 * 3300
    return data_mV

def convert_adc_array_to_mV(data_adc_array):
    data_mV_array = []
    for data_adc in data_adc_array:
        data_mV = data_adc / 4095 * 3300
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