from PyQt5 import QtWidgets, QtCore

from pyjeopardy.config import COLORS
from pyjeopardy.game import Player

class JeopardyPlayersWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')

        super(JeopardyPlayersWidget, self).__init__(*args, **kwargs)

        # list
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.itemSelectionChanged.connect(self.update_buttons)

        # title
        title = QtWidgets.QLabel('Players')

        # add button
        self.addButton = QtWidgets.QPushButton("Add")
        self.addButton.clicked.connect(self.add_player)

        # edit button
        self.editButton = QtWidgets.QPushButton("Edit")
        self.editButton.clicked.connect(self.edit_player)

        # delete button
        self.deleteButton = QtWidgets.QPushButton("Delete")
        self.deleteButton.clicked.connect(self.delete_player)

        # layout
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(title)
        vbox.addWidget(self.listWidget)
        vbox.addWidget(self.addButton)
        vbox.addWidget(self.editButton)
        vbox.addWidget(self.deleteButton)

        self.setLayout(vbox)

        self.update_buttons()

    def add_player(self):
        dialog = EditPlayerDialog(self._game, self)
        dialog.exec_()

        self.update()
        self.parent().update_play_status()

    def edit_player(self):
        player = self._get_sel_player()
        if not player:
            return  # should not happen since button is disabled

        dialog = EditPlayerDialog(self._game, self, player=player)
        dialog.exec_()

        self.update()

    def delete_player(self):
        player = self._get_sel_player()
        if not player:
            return  # should not happen since button is disabled

        text = "Delete player {}?".format(player.name)
        msg = QtWidgets.QMessageBox.question(self, "Delete player?", text,
                                             QtWidgets.QMessageBox.Yes,
                                             QtWidgets.QMessageBox.No)

        if msg == QtWidgets.QMessageBox.Yes:
            self._game.delete_player(player)
            self.update()
            self.parent().update_play_status()

    def _get_sel_player(self):
        item = self.listWidget.selectedItems()

        if len(item) != 1:
            return  None
        return item[0].data(QtCore.Qt.UserRole)

    def update(self):
        # update list
        self.listWidget.clear()
        for player in self._game.players:
            item = QtWidgets.QListWidgetItem(player.name)
            item.setData(QtCore.Qt.UserRole, player)

            self.listWidget.addItem(item)

        self.update_buttons()

    def update_buttons(self):
        # add
        if len(self._game.free_colors) != 0 and \
            self._game.is_active_hardware():

            self.addButton.setEnabled(True)
        else:
            self.addButton.setEnabled(False)

        # edit
        if self.listWidget.selectedItems():
            self.editButton.setEnabled(True)
            self.deleteButton.setEnabled(True)
        else:
            self.editButton.setEnabled(False)
            self.deleteButton.setEnabled(False)


class EditPlayerDialog(QtWidgets.QDialog):
    def __init__(self, game, parent=None, player=None):
        super(EditPlayerDialog, self).__init__(parent)

        self._game = game
        self._player = player

        # save button
        self.saveButton = QtWidgets.QPushButton("Ok")
        self.saveButton.setDefault(True);
        self.saveButton.setAutoDefault(True);
        if not self._player:
            self.saveButton.setEnabled(False)
        self.saveButton.clicked.connect(self.save)

        # cancel button
        cancelButton = QtWidgets.QPushButton("Cancel")
        cancelButton.clicked.connect(self.close)

        # name
        nameLabel = QtWidgets.QLabel("Name")
        self.nameWidget = QtWidgets.QLineEdit()
        self.nameWidget.textEdited.connect(self.update_save_button)
        if self._player:
            self.nameWidget.setText(self._player.name)

        # color
        colorLabel = QtWidgets.QLabel("Color")
        self.colorWidget = QtWidgets.QComboBox()
        if self._player:
            self.colorWidget.addItem(self._player.color.name,
                                     userData=self._player.color)
        for col in self._game.free_colors:
            self.colorWidget.addItem(col.name, userData=col)

        # key
        keyLabel = QtWidgets.QLabel("Key")
        self.keyWidget = QtWidgets.QComboBox()

        # used hardware
        hardwareLabel = QtWidgets.QLabel("Hardware")
        self.hardwareWidget = QtWidgets.QComboBox()
        self.hardwareWidget.currentIndexChanged.connect(self.update_keys)

        preadded_hw = None
        if self._player and self._player.hardware.active:
            self.hardwareWidget.addItem(self._player.hardware.name)
            preadded_hw = self._player.hardware

        for hw in self._game.hardware:
            if hw.active and hw is not preadded_hw:
                self.hardwareWidget.addItem(hw.name)

        self.update_keys()

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
        if self._player:
            self.setWindowTitle("Edit player")
        else:
            self.setWindowTitle("Add player")

    def save(self):
        name = self.nameWidget.text()
        color_index = self.colorWidget.currentIndex()
        color = self.colorWidget.itemData(color_index)
        hardware = self.get_sel_hardware()
        key_name = self.keyWidget.currentText()
        key = hardware.get_key_for_name(key_name)

        if self._player:
            self._player.name = name
            self._player.color = color
            self._player.hardware = hardware
            self._player.key = key
        else:
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
        hw = self.get_sel_hardware()
        used_keys = self._game.used_keys_for_hardware(hw)

        self.keyWidget.clear()

        if self._player and self._player.hardware == hw:
            self.keyWidget.addItem(hw.all_keys[self._player.key])

        for key, name in hw.all_keys.items():
            if key not in used_keys:
                self.keyWidget.addItem(name)

    def update_save_button(self, text):
        if text:
            self.saveButton.setEnabled(True)
        else:
            self.saveButton.setEnabled(False)
