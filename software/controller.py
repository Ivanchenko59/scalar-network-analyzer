from PySide6.QtCore import QMutex, QObject, QThread, QTimer, QWaitCondition, Signal
from PySide6.QtWidgets import QApplication, QMessageBox
import serial.tools.list_ports

from main_window import MainWindow
from device import Device

import time
import numpy as np


class Controller:
    def __init__(self):

        # gui
        self.app = QApplication([])
        self.main_window = MainWindow(controller=self)

        # device
        self.device = Device()

        # on app exit
        self.app.aboutToQuit.connect(self.on_app_exit)

    def run_app(self):
        self.main_window.show()
        return self.app.exec_()

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
            # self.worker_wait_condition.notify_one()
            return True
        else:
            self.show_no_connection_message()
            return False

    def analyzer_continuous_run(self):
        if self.device.is_connected():
            # self.timestamp_last_capture = time.time()
            # self.spf = 1
            # self.fps_timer.start(500)
            self.continuous_acquisition = True
            self.device.clean_buffers()
            # self.worker_wait_condition.notify_one()
            return True
        else:
            self.show_no_connection_message()
            return False

    def analyzer_stop(self):
        self.continuous_acquisition = False
        # self.fps_timer.stop()


    def on_app_exit(self):
        print("exiting")

