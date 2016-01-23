from PySide import QtGui, QtCore
from math import floor

from pyjeopardy.config import NUM_PLAYERS_IN_ROW

class JeopardyPointsWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')

        super(JeopardyPointsWidget, self).__init__(*args, **kwargs)

        # layout
        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)

        # add players
        self._player_widget_map = {}

        for num, player in enumerate(self._game.players):
            tmp = PlayerWidget(player=player)
            self._player_widget_map[player] = tmp

            y = num % NUM_PLAYERS_IN_ROW
            x = floor(num / NUM_PLAYERS_IN_ROW)

            self.grid.addWidget(tmp, x, y)

    def update(self):
        for player in self._player_widget_map:
            self._player_widget_map[player].update()

class PlayerWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        self._player = kwargs.pop('player')

        super(PlayerWidget, self).__init__(*args, **kwargs)

        # set background color
        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), self._player.color)
        self.setPalette(p)

        # name
        self.name = QtGui.QLabel(self._player.name)

        # points
        self.points = QtGui.QLabel(str(self._player.points))

        # layout
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.name)
        hbox.addWidget(self.points, alignment=QtCore.Qt.AlignRight)

        self.setLayout(hbox)

    def update(self):
        self.points.setText(str(self._player.points))
