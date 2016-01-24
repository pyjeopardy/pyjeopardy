from PyQt5 import QtGui, QtWidgets
from pyjeopardy.game import Game, HardwareError
from .control import JeopardyControlWidget, HardwareDialog
from .game import JeopardyGameWidget, JeopardyAnswerWidget

class JeopardyMain(QtWidgets.QMainWindow):
    def __init__(self):
        super(JeopardyMain, self).__init__()

        self._game = Game()

        self.initUI()

    def initUI(self):
        # menu
        self._add_menu()

        # widgets
        self.controlWidget = JeopardyControlWidget(game=self._game, main=self)

        # window content
        self.content = QtWidgets.QStackedWidget(self);
        self.content.addWidget(self.controlWidget)
        self.content.setCurrentWidget(self.controlWidget)

        self.setCentralWidget(self.content)

        # window title
        self.setWindowTitle('PyJeopardy')

        # show
        self.show()


    def _add_menu(self):
        menubar = self.menuBar()

        # menu -> game
        gameMenu = menubar.addMenu('&Game')

        # menu -> game -> abort game
        self.abortGameAction = QtWidgets.QAction('&Abort', self)
        self.abortGameAction.triggered.connect(self.stop_game)
        self.abortGameAction.setEnabled(False)
        gameMenu.addAction(self.abortGameAction)

        # menu -> game -> hardware
        hardwareAction = QtWidgets.QAction('&Hardware', self)
        hardwareAction.triggered.connect(self.configure_hardware)
        gameMenu.addAction(hardwareAction)

        # menu -> game -> exit
        exitAction = QtWidgets.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.triggered.connect(self.close)
        gameMenu.addAction(exitAction)

        # menu -> config
        configMenu = menubar.addMenu('&Configuration')

        # menu -> config -> load
        loadConfigAction = QtWidgets.QAction('&Load', self)
        configMenu.addAction(loadConfigAction)

        # menu -> config -> save
        saveConfigAction = QtWidgets.QAction('&Save', self)
        configMenu.addAction(saveConfigAction)

    def start_game(self):
        # get currently selected round
        cur_round = self.controlWidget.get_selected_round()

        # create widget
        gameWidget = JeopardyGameWidget(game=self._game, round=cur_round,
                                        main=self)
        self.content.addWidget(gameWidget)
        self.content.setCurrentWidget(gameWidget)

        # update menu
        self.abortGameAction.setEnabled(True)

    def stop_game(self):
        # delete widgets
        self._close_all_widgets()

        # update menu
        self.abortGameAction.setEnabled(False)

    def show_answer(self, answerwidget):
        self.content.addWidget(answerwidget)
        self.content.setCurrentWidget(answerwidget)

    def close_answer(self):
        tmp = self.content.currentWidget()

        if type(tmp) == JeopardyAnswerWidget:
            self._close_cur_widget()

    def configure_hardware(self):
        dialog = HardwareDialog(self._game, self)
        dialog.exec_()

        self.controlWidget.update_buttons()

    def _close_cur_widget(self):
        tmp = self.content.currentWidget()

        # do not delete control widget
        if tmp == self.controlWidget:
            return False

        self.content.removeWidget(tmp)
        return True

    def _close_all_widgets(self):
        while self._close_cur_widget():
            pass
