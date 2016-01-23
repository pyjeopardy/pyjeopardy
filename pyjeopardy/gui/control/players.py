from PySide import QtGui

from pyjeopardy.config import COLORS, get_color_for_name
from pyjeopardy.game import Player

class JeopardyPlayersWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')

        super(JeopardyPlayersWidget, self).__init__(*args, **kwargs)

        # list
        self.listWidget = QtGui.QListWidget(self)

        # title
        title = QtGui.QLabel('Players')

        # play button
        self.addButton = QtGui.QPushButton("Add")
        self.addButton.clicked.connect(self.add_player)

        # layout
        vbox = QtGui.QVBoxLayout()
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
            self.listWidget.addItem(QtGui.QListWidgetItem(player.name))

        # update "Add" button
        if len(self._game.free_colors) == 0:
            self.addButton.setEnabled(False)

class AddPlayerDialog(QtGui.QDialog):
    def __init__(self, game, parent=None):
        super(AddPlayerDialog, self).__init__(parent)

        self._game = game

        # name
        nameLabel = QtGui.QLabel("Name")
        self.nameWidget = QtGui.QLineEdit()
        self.nameWidget.textEdited.connect(self.update_save_button)

        # color
        colorLabel = QtGui.QLabel("Color")
        self.colorWidget = QtGui.QComboBox()
        for col in self._game.free_colors:
            self.colorWidget.addItem(col[0])

        # save
        self.saveButton = QtGui.QPushButton("Ok")
        self.saveButton.setDefault(True);
        self.saveButton.setAutoDefault(True);
        self.saveButton.setEnabled(False)
        self.saveButton.clicked.connect(self.add)

        # cancel
        cancelButton = QtGui.QPushButton("Cancel")
        cancelButton.clicked.connect(self.close)

        # layout
        grid = QtGui.QGridLayout()

        grid.addWidget(nameLabel, 1, 0)
        grid.addWidget(self.nameWidget, 1, 1)

        grid.addWidget(colorLabel, 2, 0)
        grid.addWidget(self.colorWidget, 2, 1)

        grid.addWidget(cancelButton, 3, 0)
        grid.addWidget(self.saveButton, 3, 1)

        self.setLayout(grid)

        # window title
        self.setWindowTitle("Add player")

    def add(self):
        name = self.nameWidget.text()
        color_name = self.colorWidget.currentText()
        color = get_color_for_name(color_name)

        player = Player(name, color)

        self._game.add_player(player)

        self.close()

    def update_save_button(self, text):
        if text:
            self.saveButton.setEnabled(True)
        else:
            self.saveButton.setEnabled(False)
