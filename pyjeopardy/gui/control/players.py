from PyQt5 import QtWidgets

from pyjeopardy.config import COLORS, get_color_for_name
from pyjeopardy.game import Player

class JeopardyPlayersWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')

        super(JeopardyPlayersWidget, self).__init__(*args, **kwargs)

        # list
        self.listWidget = QtWidgets.QListWidget(self)

        # title
        title = QtWidgets.QLabel('Players')

        # play button
        self.addButton = QtWidgets.QPushButton("Add")
        self.addButton.clicked.connect(self.add_player)

        # layout
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(title)
        vbox.addWidget(self.listWidget)
        vbox.addWidget(self.addButton)

        self.setLayout(vbox)

    def add_player(self):
        dialog = AddPlayerDialog(self._game, self)
        dialog.exec_()

        self.update()
        self.parent().update_play_status()

    def update(self):
        # update list
        self.listWidget.clear()
        for player in self._game.players:
            self.listWidget.addItem(QtWidgets.QListWidgetItem(player.name))

        self.update_add_status()

    def update_add_status(self):
        if len(self._game.free_colors) != 0 and \
            self._game.is_active_hardware():

            self.addButton.setEnabled(True)
        else:
            self.addButton.setEnabled(False)

class AddPlayerDialog(QtWidgets.QDialog):
    def __init__(self, game, parent=None):
        super(AddPlayerDialog, self).__init__(parent)

        self._game = game

        # name
        nameLabel = QtWidgets.QLabel("Name")
        self.nameWidget = QtWidgets.QLineEdit()
        self.nameWidget.textEdited.connect(self.update_save_button)

        # color
        colorLabel = QtWidgets.QLabel("Color")
        self.colorWidget = QtWidgets.QComboBox()
        for col in self._game.free_colors:
            self.colorWidget.addItem(col[0])

        # key
        keyLabel = QtWidgets.QLabel("Key")
        self.keyWidget = QtWidgets.QComboBox()

        # used hardware
        hardwareLabel = QtWidgets.QLabel("Hardware")
        self.hardwareWidget = QtWidgets.QComboBox()
        self.hardwareWidget.currentIndexChanged.connect(self.update_keys)
        for hw in self._game.hardware:
            if hw.active:
                self.hardwareWidget.addItem(hw.name)

        self.update_keys()

        # save
        self.saveButton = QtWidgets.QPushButton("Ok")
        self.saveButton.setDefault(True);
        self.saveButton.setAutoDefault(True);
        self.saveButton.setEnabled(False)
        self.saveButton.clicked.connect(self.add)

        # cancel
        cancelButton = QtWidgets.QPushButton("Cancel")
        cancelButton.clicked.connect(self.close)

        # layout
        grid = QtWidgets.QGridLayout()

        grid.addWidget(nameLabel, 1, 0)
        grid.addWidget(self.nameWidget, 1, 1)

        grid.addWidget(colorLabel, 2, 0)
        grid.addWidget(self.colorWidget, 2, 1)

        grid.addWidget(hardwareLabel, 3, 0)
        grid.addWidget(self.hardwareWidget, 3, 1)

        grid.addWidget(keyLabel, 4, 0)
        grid.addWidget(self.keyWidget, 4, 1)

        grid.addWidget(cancelButton, 5, 0)
        grid.addWidget(self.saveButton, 5, 1)

        self.setLayout(grid)

        # window title
        self.setWindowTitle("Add player")

    def add(self):
        name = self.nameWidget.text()
        color_name = self.colorWidget.currentText()
        color = get_color_for_name(color_name)
        hardware = self.get_sel_hardware()
        key_name = self.keyWidget.currentText()
        key = hardware.get_key_for_name(key_name)

        player = Player(name, color, hardware, key)

        self._game.add_player(player)

        self.close()

    def get_sel_hardware(self):
        hwname = self.hardwareWidget.currentText()
        for hw in self._game.hardware:
            if hw.name == hwname:
                return hw
        return None

    def update_keys(self):
        self.keyWidget.clear()
        for key, name in self.get_sel_hardware().all_keys.items():
            self.keyWidget.addItem(name)

    def update_save_button(self, text):
        if text:
            self.saveButton.setEnabled(True)
        else:
            self.saveButton.setEnabled(False)
