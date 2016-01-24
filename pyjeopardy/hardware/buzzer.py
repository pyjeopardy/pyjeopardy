from pyjeopardy.game import Hardware, HardwareError

from PyQt5 import QtWidgets

import serial.tools.list_ports

class Buzzer(Hardware):
    def __init__(self):
        super(Buzzer, self).__init__("Buzzer")

        self.configdialog = BuzzerConfigDialog

        self.tty = ""

        for key in range(1, 21):
            self.all_keys[key] = str(key)

    def init(self):
        pass

    def detect_ttys(self):
        result = []
        for tty in serial.tools.list_ports.comports():
            result.append((tty.device, tty.description))

            # try auto detection using the description
            #if not self.tty:
            #    self.tty = tty.device
        return result

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
        saveButton.setDefault(True);
        saveButton.setAutoDefault(True);
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
