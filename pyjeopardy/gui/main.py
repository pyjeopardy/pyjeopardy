from PySide import QtGui
from pyjeopardy.game import Game
from .widgets import JeopardyControlWidget, JeopardyGameWidget

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

        # menu -> game -> load config
        loadConfigAction = QtGui.QAction('&Load config', self)
        fileMenu.addAction(loadConfigAction)

        # menu -> game -> save config
        saveConfigAction = QtGui.QAction('&Save config', self)
        fileMenu.addAction(saveConfigAction)

        # menu -> game -> exit
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # widgets
        self.controlWidget = JeopardyControlWidget(game=self._game, main=self)
        self.gameWidget = JeopardyGameWidget(game=self._game)

        # window content
        self.content = QtGui.QStackedWidget(self);
        self.content.addWidget(self.controlWidget)
        self.content.addWidget(self.gameWidget)

        self.setCentralWidget(self.content)

        # window title
        self.setWindowTitle('PyJeopardy')

        # show
        self.show()

    def start_game(self):
        self.content.setCurrentWidget(self.gameWidget)
