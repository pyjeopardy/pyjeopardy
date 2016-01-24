from PyQt5 import QtGui, QtCore, QtWidgets

class HardwareItem(QtGui.QStandardItem):
    def __init__(self, *args, **kwargs):
        self.hardware = kwargs.pop('hardware')

        super(HardwareItem, self).__init__(*args, **kwargs)

class HardwareDialog(QtWidgets.QDialog):
    def __init__(self, game, parent=None):
        super(HardwareDialog, self).__init__(parent)

        self._game = game

        # item model
        self.listmodel = QtGui.QStandardItemModel(0, 1)
        self.listmodel.itemChanged.connect(self.activate_hardware)

        # list
        self.listWidget = QtWidgets.QListView()
        self.listWidget.setModel(self.listmodel)

        # add hardware to table
        for hw in self._game.hardware:
            item = HardwareItem(hw.name, hardware=hw)
            item.setCheckable(True)

            if hw.active:
                item.setCheckState(QtCore.Qt.Checked)

            self.listmodel.appendRow(item)

        # edit button
        configureButton = QtWidgets.QPushButton("Configure")
        configureButton.clicked.connect(self.configure)

        # ok button
        okButton = QtWidgets.QPushButton("Ok")
        okButton.clicked.connect(self.close)

        # layout
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.listWidget)
        vbox.addWidget(configureButton)
        vbox.addWidget(okButton)

        self.setLayout(vbox)

        # window title
        self.setWindowTitle("Configure hardware")

    def activate_hardware(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            item.hardware.active = True
        else:
            item.hardware.active = False

    def configure(self):
        index = self.listWidget.currentIndex()
        item = self.listmodel.itemFromIndex(index)
        hardware = item.hardware

        if hardware.configdialog:
            dialog = hardware.configdialog(hardware)
            dialog.exec_()
