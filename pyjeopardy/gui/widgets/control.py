from PySide import QtGui

from .rounds import JeopardyRoundsWidget
from .players import JeopardyPlayersWidget

class JeopardyControlWidget(QtGui.QWidget):
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
        playButton = QtGui.QPushButton("Play")
        playButton.clicked.connect(self._main.start_game)

        # layout: place rounds and players horizontally
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.roundsWidget)
        hbox.addWidget(self.playersWidget)

        # layout: play button on the bottom
        vbox = QtGui.QVBoxLayout(self)
        vbox.addLayout(hbox)
        vbox.addWidget(playButton)

        self.setLayout(vbox)
