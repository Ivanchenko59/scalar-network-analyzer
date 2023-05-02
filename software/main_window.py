from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QMainWindow,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QSizePolicy,
    QDialog,
    QCheckBox,
)
import pyqtgraph as pg
from utils import convert_MHz_to_Hz, convert_Hz_to_MHz, convert_points_to_freq_step, convert_freq_step_to_points

from datatypes import Data 
from datatypes import PointType 


class AnalyzerScreen(pg.PlotWidget):
    def __init__(self, parent=None, plotItem=None, **kargs):
        super().__init__(parent=parent, background="w", plotItem=plotItem, **kargs)
        
        self.plot_map = {}

        styles = {"color": "k", "font-size": "14px"}
        self.setLabel("left", "dB", **styles)
        self.setLabel("bottom", "Frequency", **styles)

        self.showGrid(x=True, y=True)
        self.setXRange(0, 145000000, padding=0.02)
        self.setYRange(-70, 0, padding=0.02)
        self.setLimits(xMin=-0.1, xMax=500000000)
        self.setLimits(yMin=-100, yMax=20)

        self.pen_ch = pg.mkPen(color="b", width=1.5)

    def plot_ch(self, x, y, plot_name='default', pen1=None):
        if pen1 is None:
            pen1 = self.pen_ch
        self.plot_map[plot_name] = self.plot(x, y, pen=pen1)
    
    def clear_ch(self, plot_name='default'):
        if plot_name in self.plot_map:
            self.plot_map[plot_name].clear()

    def set_axis(self, min, max):
        # self.setLimits(xMin=min, xMax=max)
        # self.setXRange(min, max, padding=0.02)
        pass


class SpinBox(QGroupBox):
    def __init__(self, controller, analyzer_screen, parent=None):
        super().__init__("Frequency", parent=parent)
        self.controller = controller
        self.analyzer_screen = analyzer_screen

        layout = QVBoxLayout()
        self.setLayout(layout)

        min_freq_layout = QHBoxLayout()
        min_freq_label = QLabel("Min (MHz):")
        self.spinbox_min_freq = QDoubleSpinBox()
        self.spinbox_min_freq.setDecimals(3)
        self.spinbox_min_freq.setRange(
            convert_Hz_to_MHz(self.controller.get_min_freq_in_Hz()), 
            convert_Hz_to_MHz(self.controller.get_max_freq_in_Hz())
            )
        self.spinbox_min_freq.setValue(convert_Hz_to_MHz(self.controller.get_min_freq_in_Hz()))
        min_freq_layout.addWidget(min_freq_label)
        min_freq_layout.addWidget(self.spinbox_min_freq)

        max_freq_layout = QHBoxLayout()
        max_freq_label = QLabel("Max(MHz):")
        self.spinbox_max_freq = QDoubleSpinBox()
        self.spinbox_max_freq.setDecimals(3)
        self.spinbox_max_freq.setRange(
            convert_Hz_to_MHz(self.controller.get_min_freq_in_Hz()), 
            convert_Hz_to_MHz(self.controller.get_max_freq_in_Hz())
            )
        self.spinbox_max_freq.setValue(convert_Hz_to_MHz(self.controller.get_max_freq_in_Hz()))
        max_freq_layout.addWidget(max_freq_label)
        max_freq_layout.addWidget(self.spinbox_max_freq)

        step_freq_layout = QHBoxLayout()
        step_freq_label = QLabel("Points:")
        self.spinbox_step_freq = QSpinBox()
        self.spinbox_step_freq.setRange(1, 1000000)
        self.spinbox_step_freq.setValue(
            convert_freq_step_to_points(self.controller.get_min_freq_in_Hz(),
                                        self.controller.get_max_freq_in_Hz(),
                                        self.controller.get_step_freq()
                                        ))
                                        
        step_freq_layout.addWidget(step_freq_label)
        step_freq_layout.addWidget(self.spinbox_step_freq)

        layout.addLayout(min_freq_layout)
        layout.addLayout(max_freq_layout)
        layout.addLayout(step_freq_layout)

        self.spinbox_min_freq.valueChanged.connect(self.on_spinbox_min_freq_value_changed)
        self.spinbox_max_freq.valueChanged.connect(self.on_spinbox_max_freq_value_changed)
        self.spinbox_step_freq.valueChanged.connect(self.on_spinbox_step_freq_value_changed)

    def on_spinbox_min_freq_value_changed(self, value):
        self.controller.set_min_freq(convert_MHz_to_Hz(value))
        # self.analyzer_screen.set_axis(value, 20000)
        print(value)

    def on_spinbox_max_freq_value_changed(self, value):
        self.controller.set_max_freq(convert_MHz_to_Hz(value))
        print(value)

    def on_spinbox_step_freq_value_changed(self, value):
        self.controller.set_step_freq(
            convert_points_to_freq_step(self.controller.get_min_freq_in_Hz(),
                                        self.controller.get_max_freq_in_Hz(),
                                        value
                                        ))
        print(value)


class CalibrationBox(QGroupBox):
    def __init__(self, controller, parent=None):
        super().__init__("Calibration", parent=parent)
        self.controller = controller

        # self.is_running = False

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.button_calibrate = QPushButton("Calibrate")

        layout.addWidget(self.button_calibrate)

        self.button_calibrate.clicked.connect(self.on_calibrate_button)

    def on_calibrate_button(self):
        self.controller.analyzer_calibration_mode()
        print("Calibrated")


class AcquisitionBox(QGroupBox):
    def __init__(self, controller, parent=None):
        super().__init__("Acquisition", parent=parent)
        self.controller = controller

        self.is_running = False

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.button_single = QPushButton("SINGLE")
        self.button_run = QPushButton("RUN")

        layout.addWidget(self.button_single)
        layout.addWidget(self.button_run)

        self.button_run.clicked.connect(self.on_run_stop_button)
        self.button_single.clicked.connect(self.on_single_button)

    def on_single_button(self):
        self.controller.analyzer_single_run()
        self.is_running = False
        self.button_run.setText("RUN")

    def on_run_stop_button(self):
        if self.is_running:
            self.controller.analyzer_stop()
            self.is_running = False
            self.button_run.setText("RUN")
        else:
            if self.controller.analyzer_continuous_run():
                self.is_running = True
                self.button_run.setText("STOP")


class DeviceBox(QGroupBox):
    def __init__(self, controller, parent=None):
        super().__init__("Device", parent=parent)
        self.controller = controller

        self.is_connected = False

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.button_refresh = QPushButton("Refresh")
        self.combobox_ports = QComboBox()
        self.button_connect = QPushButton("Connect")

        layout.addWidget(self.button_refresh)
        layout.addWidget(self.combobox_ports)
        layout.addWidget(self.button_connect)

        self.button_refresh.clicked.connect(self.refresh_ports)
        self.button_connect.clicked.connect(self.connect_to_device)

    def refresh_ports(self):
        self.combobox_ports.clear()
        self.combobox_ports.addItems(self.controller.get_ports_names())

    def connect_to_device(self):

        if not self.is_connected:
            port = self.combobox_ports.currentText()
            self.controller.connect_to_device(port)
        else:
            self.controller.disconnect_device()

        self.is_connected = self.controller.is_device_connected()
        if self.is_connected:
            self.button_connect.setText("Disconnect")
        else:
            self.button_connect.setText("Connect")



class DebugButton(QPushButton):
    def __init__(self, controller, analyzer_screen, parent=None):
        super().__init__("Debug", parent=parent)

        self.controller = controller
        self.analyzer_screen = analyzer_screen
        
        self.clicked.connect(self.on_debug_button_clicked)
        self.debug_window = DebugWindow(self.controller, self.analyzer_screen)

    def on_debug_button_clicked(self):
        self.debug_window.exec_()

class DebugWindow(QDialog):
    def __init__(self, controller, analyzer_screen, parent=None):
        super().__init__(parent)

        self.controller = controller
        self.analyzer_screen = analyzer_screen

        self.setWindowTitle("Debug")
        self.setMinimumSize(200, 100)

        layout = QVBoxLayout(self)
        self.frequency_spinbox = QSpinBox()
        self.frequency_spinbox.setObjectName("frequency_spinbox")
        self.frequency_spinbox.setRange(1, 500000000)
        self.frequency_spinbox.setValue(1000)
        self.frequency_spinbox.setSingleStep(100)

        layout.addWidget(self.frequency_spinbox)

        self.raw_adc_checkbox = QCheckBox("Raw dB data")
        self.raw_adc_checkbox.setObjectName("raw_dB_checkbox")
        self.raw_adc_checkbox.setChecked(False)
        layout.addWidget(self.raw_adc_checkbox)

        self.raw_dbm_checkbox = QCheckBox("Filtered dB data")
        self.raw_dbm_checkbox.setObjectName("filtered_dB_checkbox")
        self.raw_dbm_checkbox.setChecked(False)
        layout.addWidget(self.raw_dbm_checkbox)

        self.calibration_json_checkbox = QCheckBox("Calibration JSON data")
        self.calibration_json_checkbox.setObjectName("calibration_json_checkbox")
        self.calibration_json_checkbox.setChecked(False)
        layout.addWidget(self.calibration_json_checkbox)

        self.frequency_spinbox.valueChanged.connect(self.on_frequency_changed)
        self.raw_adc_checkbox.stateChanged.connect(self.on_checkbox_changed)
        self.raw_dbm_checkbox.stateChanged.connect(self.on_checkbox_changed)
        self.calibration_json_checkbox.stateChanged.connect(self.on_checkbox_changed)


    def on_frequency_changed(self, value):
        self.controller.measure_at_freq(value)

    def on_checkbox_changed(self, state):
        checkbox_name = self.sender().objectName()
        # TODO: Qt.Checked is shit
        if state == 2:
            if checkbox_name == "raw_dB_checkbox":
                self.analyzer_screen.plot_ch(
                    self.controller.raw_data.frequency, 
                    self.controller.raw_data.convert_to(PointType.DB), 
                    checkbox_name, 
                    pg.mkPen(color="r", width=1.5)
                )
            elif checkbox_name == "filtered_dB_checkbox":
                self.analyzer_screen.plot_ch(
                    self.controller.filtered_data.frequency, 
                    self.controller.filtered_data.convert_to(PointType.DB), 
                    checkbox_name,
                    pg.mkPen(color="g", width=1.5)
                )
            elif checkbox_name == "calibration_json_checkbox":
                # self.calibration_json_data_curve.show()
                pass
        else:
            self.analyzer_screen.clear_ch(checkbox_name)


class ControlPanel(QFrame):
    def __init__(self, controller, analyzer_screen, parent=None):
        super().__init__(parent=parent)
        self.controller = controller
        self.analyzer_screen = analyzer_screen

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setMinimumWidth(180)
        self.setMaximumWidth(320)

        # widgets here
        self.freq_panel = SpinBox(self.controller, self.analyzer_screen)
        self.calibr_panel = CalibrationBox(self.controller)
        self.acq_panel = AcquisitionBox(self.controller)
        self.dev_panel = DeviceBox(self.controller)
        self.layout = QVBoxLayout()
        self.debug_panel = DebugButton(self.controller, self.analyzer_screen)

        # widgets here
        self.layout.addWidget(self.calibr_panel)
        self.layout.addWidget(self.freq_panel)
        self.layout.addWidget(self.acq_panel)
        self.layout.addStretch()

        self.layout.addWidget(self.dev_panel)
        self.layout.addWidget(self.debug_panel)

        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controller = controller

        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Scalar Network Analyzer")

        self.screen = AnalyzerScreen()
        self.screen.setMinimumWidth(650)
        self.control_panel = ControlPanel(self.controller, self.screen)

        self.content_layout = QHBoxLayout()
        self.content_layout.addWidget(self.screen)
        self.content_layout.addWidget(self.control_panel)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.content_layout)
