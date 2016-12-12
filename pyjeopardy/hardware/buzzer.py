from pyjeopardy.game import Hardware, HardwareError
from pyjeopardy.config import HARDWARE_POLLINTERVAL

from PyQt5 import QtWidgets, QtCore

import serial
import serial.tools.list_ports


class Buzzer(Hardware):
    HW_DESCRIPTION = 'Arduino Micro'

    def __init__(self):
        super(Buzzer, self).__init__("Buzzer")

        self.configdialog = BuzzerConfigDialog

        self.tty = ""

        self._ser = None

        self._input_buffer = ""

        self._timer = QtCore.QTimer()
        self._timer.setInterval(HARDWARE_POLLINTERVAL)
        self._timer.timeout.connect(self.update)
        self._timer.start()

        self._callback = None

        for key in range(1, 19):
            self.all_keys[key] = str(key)

        # trigger auto detection
        self.detect_ttys()

    def detect_ttys(self):
        result = []
        for tty in serial.tools.list_ports.comports():
            result.append((tty.device, tty.description))

            # try auto detection
            if not self.tty and Buzzer.HW_DESCRIPTION in tty.description:
                self.tty = tty.device
        return result

    def connect(self):
        if self.tty:
            try:
                self._ser = serial.Serial(self.tty)
            except serial.SerialException as e:
                raise HardwareError(self, "Cannot connect: " + str(e))
        else:
            raise HardwareError(self, "No serial port selected")

        self.stop()

    def disconnect(self):
        if self._ser:
            try:
                self._ser.write(b'reset\n')
            except serial.SerialException as e:
                raise HardwareError(self, "Cannot send command: " + str(e))

            try:
                self._ser.close()
            except serial.SerialException as e:
                raise HardwareError(self, "Cannot close connection: " + str(e))

            self._ser = None

    def start(self, callback):
        if self._ser:
            try:
                self._ser.write(b'start\n')
            except serial.SerialException as e:
                raise HardwareError(self, "Cannot send command: " + str(e))

            self._callback = callback

    def stop(self):
        if self._ser:
            try:
                self._ser.write(b'reset\n')
            except serial.SerialException as e:
                raise HardwareError(self, "Cannot send command: " + str(e))

    def update(self):
        if self.active and self._ser:
            try:
                # read waiting bytes
                count = self._ser.in_waiting
                if count > 0:
                    self._input_buffer += self._ser.read(count).decode("utf-8")

                if self._input_buffer:
                    # split in lines
                    tmp = self._input_buffer.split('\n')

                    if self._input_buffer.endswith('\n'):
                        self._input_buffer = ""
                    else:
                        self._input_buffer = tmp.pop()

                    # handle lines
                    while len(tmp) > 0:
                        input_str = tmp.pop(0)

                        if input_str != "ready" and input_str != "":
                            try:
                                number = int(input_str)

                                self._callback(self, number)
                            except ValueError as e:
                                raise HardwareError(self, "Invalid response "
                                                    "from hardware" + str(e))
            except (serial.SerialException, OSError) as e:
                pass  # TODO: better error handling, maybe set a flag?


class BuzzerConfigDialog(QtWidgets.QDialog):
    def __init__(self, hardware, parent=None):
        super(BuzzerConfigDialog, self).__init__(parent)

        self._buzzer = hardware

        # tty
        ttyLabel = QtWidgets.QLabel("TTY")
        ttys = self._buzzer.detect_ttys()
        self.ttyWidget = QtWidgets.QComboBox()
        for tty in ttys:
            self.ttyWidget.addItem("{} - {}".format(*tty), tty[0])
        self.ttyWidget.addItem("Custom path", None)

        # custom tty
        self.customttyWidget = QtWidgets.QLineEdit()

        # set selected tty
        new_sel_index = self.ttyWidget.findData(self._buzzer.tty)
        if new_sel_index != -1:
            self.ttyWidget.setCurrentIndex(new_sel_index)
            self.customttyWidget.hide()
        else:
            # custom tty
            self.customttyWidget.setText(self._buzzer.tty)
            self.ttyWidget.setCurrentIndex(self.ttyWidget.count()-1)

        # and now the event handler
        self.ttyWidget.currentIndexChanged.connect(self.update_custom_field)

        # save
        saveButton = QtWidgets.QPushButton("Save")
        saveButton.setDefault(True)
        saveButton.setAutoDefault(True)
        saveButton.clicked.connect(self.save)

        # cancel
        cancelButton = QtWidgets.QPushButton("Cancel")
        cancelButton.clicked.connect(self.close)

        # layout
        grid = QtWidgets.QGridLayout()

        grid.addWidget(ttyLabel, 1, 0)
        grid.addWidget(self.ttyWidget, 1, 1)

        grid.addWidget(self.customttyWidget, 2, 1)

        grid.addWidget(cancelButton, 3, 0)
        grid.addWidget(saveButton, 3, 1)

        self.setLayout(grid)

        # window title
        self.setWindowTitle("Configure buzzer hardware")

    def save(self):
        tty = self._selected_tty()
        if not tty:
            tty = self.customttyWidget.text()

        self._buzzer.tty = tty

        self.close()

    def update_custom_field(self):
        if self._selected_tty():
            self.customttyWidget.hide()
        else:
            self.customttyWidget.show()

    def _selected_tty(self):
        return self.ttyWidget.itemData(self.ttyWidget.currentIndex())
