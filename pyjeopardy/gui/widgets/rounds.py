from PySide import QtGui

class JeopardyRoundsWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')

        super(JeopardyRoundsWidget, self).__init__(*args, **kwargs)

        # list
        self.listWidget = QtGui.QListWidget(self)

        # title
        title = QtGui.QLabel('Rounds')

        # play button
        playButton = QtGui.QPushButton("Play")

        # layout
        hbox = QtGui.QVBoxLayout()
        hbox.addWidget(title)
        hbox.addWidget(self.listWidget)
        hbox.addWidget(playButton)

        self.setLayout(hbox)

        self.update()

    def update(self):
        self.listWidget.clear()

        for round in self._game.rounds:
            QtGui.QListWidgetItem(round.name, self.listWidget)
