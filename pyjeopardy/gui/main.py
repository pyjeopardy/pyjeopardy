from PySide import QtGui

class JeopardyMain(QtGui.QMainWindow):
    def __init__(self):
        super(JeopardyMain, self).__init__()

        self.initUI()

    def initUI(self):
        #self.statusBar().showMessage('Ready')
        menubar = self.menuBar()

        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.setWindowTitle('PyJeopardy')
        self.show()
