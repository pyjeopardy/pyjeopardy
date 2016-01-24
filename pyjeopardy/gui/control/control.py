from PyQt5 import QtWidgets

from .rounds import JeopardyRoundsWidget
from .players import JeopardyPlayersWidget

class JeopardyControlWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')
        self._main = kwargs.pop('main')

        super(JeopardyControlWidget, self).__init__(*args, **kwargs)

        # rounds widget
        self.roundsWidget = JeopardyRoundsWidget(game=self._game,
                                                 main=self._main)

        # players widget
        self.playersWidget = JeopardyPlayersWidget(game=self._game)

        # play button
        self.playButton = QtWidgets.QPushButton("Play")
        self.playButton.setEnabled(False)
        self.playButton.clicked.connect(self._main.start_game)

        # layout: place rounds and players horizontally
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.roundsWidget)
        hbox.addWidget(self.playersWidget)

        # layout: play button on the bottom
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addLayout(hbox)
        vbox.addWidget(self.playButton)

        self.setLayout(vbox)

    def update_play_status(self):
        if self.roundsWidget.get_selected_round() and \
            len(self._game.players) != 0:
            self.playButton.setEnabled(True)
        else:
            self.playButton.setEnabled(False)

    def get_selected_round(self):
        return self.roundsWidget.get_selected_round()
