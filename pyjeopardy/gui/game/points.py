from PyQt5 import QtCore, QtWidgets
from math import floor

from pyjeopardy.config import NUM_PLAYERS_IN_ROW, FONT_SIZE_PLAYERS


class JeopardyPointsWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')

        super(JeopardyPointsWidget, self).__init__(*args, **kwargs)

        # layout
        self.grid = QtWidgets.QGridLayout()
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


class PlayerWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        self._player = kwargs.pop('player')

        super(PlayerWidget, self).__init__(*args, **kwargs)

        # set background color
        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), self._player.color.qt)
        p.setColor(self.foregroundRole(), self._player.color.textcolor())
        self.setPalette(p)

        # font size
        self.setStyleSheet("QWidget {{ font-size: {}px; }}".format(
                            FONT_SIZE_PLAYERS))

        # name
        self.name = QtWidgets.QLabel(self._player.name)

        # points
        self.points = QtWidgets.QLabel(str(self._player.points))

        # layout
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.name)
        hbox.addWidget(self.points, alignment=QtCore.Qt.AlignRight)

        self.setLayout(hbox)

    def update(self):
        self.points.setText(str(self._player.points))
