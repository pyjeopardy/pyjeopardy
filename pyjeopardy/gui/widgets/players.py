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
        addButton = QtGui.QPushButton("Add")
        addButton.clicked.connect(self.addPlayer)

        # layout
        hbox = QtGui.QVBoxLayout()
        hbox.addWidget(title)
        hbox.addWidget(self.listWidget)
        hbox.addWidget(addButton)

        self.setLayout(hbox)

    def addPlayer(self):
        dialog = JeopardyAddPlayerDialog(self._game, self)
        dialog.exec_()

        self.update()

    def update(self):
        self.listWidget.clear()
        for player in self._game.players:
            self.listWidget.addItem(QtGui.QListWidgetItem(player.name))

class JeopardyAddPlayerDialog(QtGui.QDialog):
    def __init__(self, game, parent=None):
        super(JeopardyAddPlayerDialog, self).__init__(parent)

        self._game = game

        # name
        nameLabel = QtGui.QLabel("Name")
        self.nameWidget = QtGui.QLineEdit()

        # color
        colorLabel = QtGui.QLabel("Color")
        self.colorWidget = QtGui.QComboBox()
        for col in self._game.free_colors:
            self.colorWidget.addItem(col[0])

        # save
        saveButton = QtGui.QPushButton("Ok")
        saveButton.clicked.connect(self.add)

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
        grid.addWidget(saveButton, 3, 1)

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
