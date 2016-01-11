from PySide import QtGui
from pyjeopardy.game import Game, Round
from .widgets import JeopardyRoundsWidget, JeopardyPlayersWidget

class JeopardyMain(QtGui.QMainWindow):
    def __init__(self):
        super(JeopardyMain, self).__init__()

        self._game = Game()

        self.initUI()

    def initUI(self):
        # menu
        menubar = self.menuBar()

        # menu -> game
        fileMenu = menubar.addMenu('&Game')

        # menu -> game -> add round
        addRoundAction = QtGui.QAction('&Add round', self)
        addRoundAction.triggered.connect(self.add_round)
        fileMenu.addAction(addRoundAction)

        # menu -> game -> exit
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # window
        window = QtGui.QWidget(self)

        # rounds widget
        self.roundsWidget = JeopardyRoundsWidget(game=self._game)

        # players widget
        self.playersWidget = JeopardyPlayersWidget(game=self._game)

        # layout
        hbox = QtGui.QHBoxLayout(window)
        hbox.addWidget(self.roundsWidget)
        hbox.addWidget(self.playersWidget)

        window.setLayout(hbox)

        # set content
        self.setCentralWidget(window)

        # window title
        self.setWindowTitle('PyJeopardy')

        # show window
        self.show()

    def add_round(self):
        fname, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open file')

        if fname:
            round = Round()
            round.load(fname)

            self._game.add_round(round)

            self.roundsWidget.update()
