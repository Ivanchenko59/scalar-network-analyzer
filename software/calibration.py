import numpy as np
import json
from datatypes import Data 
from datatypes import PointType 

FILENAME = "calibration_data.json"

def write_calibration_data(data:Data):
        write_data = {
             'frequency':data.frequency,
             'points':data.points
        }
        with open(FILENAME, 'w') as f:
            json.dump(write_data, f)
            

def read_calibration_data():
    with open(FILENAME, 'r') as file:
        data = json.load(file)
    return Data(data["frequency"], data["points"], PointType.RAW)

def perform_calibration(measurement_data):
    calibration_data = read_calibration_data()
    ampl_cal_interp = np.interp(
        measurement_data.frequency, 
        calibration_data.frequency, 
        calibration_data.points
    )
    
    calibrated_data = np.subtract(
        measurement_data.convert_to(PointType.DB), 
        Data.convert_points_to(ampl_cal_interp, PointType.RAW, PointType.DB)
    )
    return Data(measurement_data.frequency, calibrated_data, PointType.DB)
