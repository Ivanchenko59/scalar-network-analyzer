from PySide6.QtCore import QMutex, QObject, QThread, QTimer, QWaitCondition, Signal, Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QProgressDialog
import serial.tools.list_ports

from main_window import MainWindow
from device import Device

import json


import time
import numpy as np

import debugpy


class Controller:
    def __init__(self):

        self.filename = "calibration_data.json"

        # gui
        self.app = QApplication([])
        self.main_window = MainWindow(controller=self)

        # device
        self.device = Device()
        
        # acquisition thread
        self.continuous_acquisition = False
        self.worker_wait_condition = QWaitCondition()
        self.acquisition_worker = AcquisitionWorker(
            self.worker_wait_condition, device=self.device
        )
        self.acquisition_thread = QThread()
        self.acquisition_worker.moveToThread(self.acquisition_thread)
        self.acquisition_thread.started.connect(self.acquisition_worker.run)
        self.acquisition_worker.finished.connect(self.acquisition_thread.quit)
        # self.acquisition_worker.finished.connect(self.acquisition_thread.deleteLater)
        # self.acquisition_thread.finished.connect(self.acquisition_worker.deleteLater)
        self.acquisition_worker.data_ready.connect(self.data_ready_callback)
        self.acquisition_thread.start()

        # on app exit
        self.app.aboutToQuit.connect(self.on_app_exit)


    def run_app(self):
        self.main_window.show()
        return self.app.exec_()

    def set_min_freq(self, min_freq):
        self.device.min_freq = min_freq

    def set_max_freq(self, max_freq):
        self.device.max_freq = max_freq

    def set_step_freq(self, step_freq):
        self.device.step_freq = step_freq

    def get_ports_names(self):
        return [p.device for p in serial.tools.list_ports.comports()]

    def connect_to_device(self, port):
        if port == "":
            QMessageBox.about(
                self.main_window,
                "Connection failed",
                "Could not connect to device. No port is selected.",
            )
        elif port not in self.get_ports_names():
            QMessageBox.about(
                self.main_window,
                "Connection failed",
                f"Could not connect to device. Port {port} not available. Refresh and try again.",
            )
        else:
            self.device.connect(port)

    def disconnect_device(self):
        self.device.disconnect()

    def is_device_connected(self):
        return self.device.is_connected()

    def show_no_connection_message(self):
        QMessageBox.about(
            self.main_window,
            "Device not connected",
            "No device is connected. Connect a device first.",
        )


    # custom slots
    def analyzer_single_run(self):
        if self.device.is_connected():
            self.continuous_acquisition = False
            self.device.clean_buffers()
            self.main_window.screen.clear_ch()
            self.worker_wait_condition.notify_one()
            return True
        else:
            self.show_no_connection_message()
            return False

    def analyzer_continuous_run(self):
        if self.device.is_connected():
            self.continuous_acquisition = True
            self.device.clean_buffers()
            # self.worker_wait_condition.notify_one()
            return True
        else:
            self.show_no_connection_message()
            return False

    def analyzer_calibration_mode(self):
        if self.device.is_connected():
            
            self.progress_dialog = QProgressDialog("Calibrating...", "Cancel", self.device.min_freq, self.device.max_freq, self.main_window)
            self.progress_dialog.setWindowTitle("Calibration Progress")
            self.progress_dialog.setWindowModality(Qt.WindowModal)
            self.progress_dialog.setCancelButton(None)
            self.progress_dialog.setAutoClose(True)
            self.progress_dialog.setAutoReset(True)
            self.progress_dialog.show()

            x_ret = []
            y_ret = []

            for freq in range(self.device.min_freq, self.device.max_freq + self.device.step_freq, self.device.step_freq):
                if self.progress_dialog.wasCanceled():
                    break
                self.progress_dialog.setValue(freq)
                QApplication.processEvents()
                
                x_ret.append(freq)
                adc_data = self.device.measure_at_freq(freq)
                y_ret.append(adc_data)

            # Save data to JSON file
            data = {"frequency": x_ret, "adc": y_ret}
            self.write_calibration_data(data)

            self.progress_dialog.close()
            return True
        else:
            self.main_window.show_no_connection_message()
            return False

    def analyzer_stop(self):
        self.continuous_acquisition = False

    def data_ready_callback(self):
        self.calibrated_data = self.perform_calibration(self.acquisition_worker.raw_data)
        self.main_window.screen.plot_ch(
            self.calibrated_data[0], self.calibrated_data[1]
        )
        if self.continuous_acquisition == True:
            self.worker_wait_condition.notify_one()

    def on_app_exit(self):
        print("exiting")

    def write_calibration_data(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def read_calibration_data(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)
        return data

    def perform_calibration(self, measurement_data):
        calibration_data = self.read_calibration_data()
        ampl_cal_interp = np.interp(measurement_data[0], calibration_data['frequency'], calibration_data['adc'])
        # calibrated_data = [x - y for x,y in zip(measurement_data[1], ampl_cal_interp)]
        calibrated_data = np.subtract(measurement_data[1], ampl_cal_interp)
        return measurement_data[0], calibrated_data

class AcquisitionWorker(QObject):

    finished = Signal()
    data_ready = Signal()

    def __init__(self, wait_condition, device, parent=None):
        super().__init__(parent=parent)
        self.wait_condition = wait_condition
        self.device = device
        self.mutex = QMutex()

    def run(self):
        # debugpy.debug_this_thread()
        while True:
            self.mutex.lock()
            self.wait_condition.wait(self.mutex)
            self.mutex.unlock()

            self.raw_data  = self.device.acquire_single()
            self.data_ready.emit()

        self.finished.emit()
