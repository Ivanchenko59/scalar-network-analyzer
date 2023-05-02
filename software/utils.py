import numpy as  np
import scipy.signal

def get_smooth_func(y_points):
    n = 7
    e = 0.15

    smoothness = 50 

    for i in range(len(y_points) - n):
        avg = sum(y_points[i:i+n])/n
        if abs((y_points[i + n//2] - avg)/y_points[i + n//2]) > e:
            y_points[i + n//2] = (n * avg - y_points[i + n//2])/(n - 1)


    rft = np.fft.rfft(y_points)
    rft[smoothness  :] = 0   # Note, rft.shape = 21
    y_smooth = np.fft.irfft(rft, len(y_points))
    return list(y_smooth)


def filter_func(y_points):
    
    return [int(x) for x in scipy.signal.medfilt(y_points).tolist()]
    


def convert_MHz_to_Hz(freq):
    return int(freq * 1000000)

def convert_Hz_to_MHz(freq):
    return freq / 1000000

def convert_points_to_freq_step(min_freq, max_freq, points):
    return int((max_freq - min_freq) / points)

def convert_freq_step_to_points(min_freq, max_freq, freq_step):
    return int((max_freq - min_freq) / freq_step)