from PyQt5 import QtWidgets

from .points import PlayerWidget


class JeopardyEndWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        self._main = kwargs.pop('main')
        self._game = kwargs.pop('game')

        super(JeopardyEndWidget, self).__init__(*args, **kwargs)

        # layout
        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        # content
        players = sorted(self._game.players, key=lambda p: p.points,
                         reverse=True)
        for player in players:
            tmp = PlayerWidget(player=player)

            vbox.addWidget(tmp)

        endButton = QtWidgets.QPushButton("End")
        endButton.clicked.connect(self.end)
        vbox.addWidget(endButton)

    def end(self):
        self._main.stop_game()
