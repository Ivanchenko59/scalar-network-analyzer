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
    QLineEdit,
    QMessageBox
)
import pyqtgraph as pg


class AnalyzerScreen(pg.PlotWidget):
    def __init__(self, parent=None, plotItem=None, **kargs):
        super().__init__(parent=parent, background="w", plotItem=plotItem, **kargs)

        styles = {"color": "k", "font-size": "12px"}
        self.setLabel("left", "V", **styles)
        self.setLabel("bottom", "f", **styles)

        self.showGrid(x=True, y=True)
        self.setXRange(0, 5, padding=0.02)
        self.setYRange(0, 5, padding=0.02)

        self.pen_ch1 = pg.mkPen(color="b", width=1)

        self.x_points = [0,1]
        self.y_points = [0,1]

        self.plot_ch(self.x_points, self.y_points)

    def plot_ch(self, x, y, ch=1):
        self.data_line_ch = self.plot(x, y, pen=self.pen_ch1)

    def update_ch(self, x, y, ch=1):
        self.x_points.extend(x)
        self.y_points.extend(y)
        self.data_line_ch.setData(self.x_points, self.y_points)



class LineEdit(QGroupBox):
    def __init__(self, controller, parent=None):
        super().__init__("Frequency", parent=parent)
        self.controller = controller

        # self.is_connected = False

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.input_low_freq = QLineEdit("Low Frequency")
        self.input_hight_freq = QLineEdit("High Frequency")
        
        layout.addWidget(self.input_low_freq)
        layout.addWidget(self.input_hight_freq)
        
        # self.input.textChanged.connect


class CalibrationBox(QGroupBox):
    def __init__(self, controller, parent=None):
        super().__init__("Calibration", parent=parent)
        self.controller = controller

        # self.is_running = False

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.button_calibrate = QPushButton("Calibrate")

        layout.addWidget(self.button_calibrate)

        # self.button_calibrate.clicked.connect(self.on_calibrate_button)

    def on_calibrate_button(self):
        # self.controller.analyzer_single_run()
        # self.is_running = False
        # self.button_run.setText("RUN")
        print("Calibration")


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


class ControlPanel(QFrame):
    def __init__(self, controller, parent=None):
        super().__init__(parent=parent)
        self.controller = controller

        self.setFrameStyle(QFrame.StyledPanel)
        self.setMaximumWidth(300)

        # widgets here
        self.freq_panel = LineEdit(self.controller)
        self.calibr_panel = CalibrationBox(self.controller)
        self.acq_panel = AcquisitionBox(self.controller)
        self.dev_panel = DeviceBox(self.controller)

        self.layout = QVBoxLayout()

        # widgets here
        self.layout.addWidget(self.freq_panel)
        self.layout.addWidget(self.calibr_panel)
        self.layout.addWidget(self.acq_panel)
        self.layout.addStretch()
        self.layout.addWidget(self.dev_panel)

        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controller = controller

        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Scalar Network Analyzer")

        self.screen = AnalyzerScreen()
        self.control_panel = ControlPanel(self.controller)

        self.content_layout = QHBoxLayout()
        self.content_layout.addWidget(self.screen)
        self.content_layout.addWidget(self.control_panel)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.content_layout)
