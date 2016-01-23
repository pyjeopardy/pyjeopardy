from PySide import QtGui, QtCore

from pyjeopardy.config import ANSWER_FONT_SIZE


class JeopardyAnswerWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')
        self._gamewidget = kwargs.pop('gamewidget')
        self._answer = kwargs.pop('answer')

        self._current_player = None

        super(JeopardyAnswerWidget, self).__init__(*args, **kwargs)

        # layout
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)

        # content
        tmp = None
        if self._answer.is_text():
            tmp = QtGui.QLabel(self._answer.get_text())
            tmp.setStyleSheet("QLabel {{ font-size: {}px; }}".format(
                ANSWER_FONT_SIZE))
        # <- add further types here

        if tmp:
            tmp.setSizePolicy(QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Expanding)
            vbox.addWidget(tmp, alignment=QtCore.Qt.AlignCenter)
        else:
            print("ERROR: unsupported answer type")

        # current player
        self.currentPlayerLabel = QtGui.QLabel("")

        # right button
        self.rightButton = QtGui.QPushButton("Right")
        self.rightButton.clicked.connect(self.right)

        # wrong button
        self.wrongButton = QtGui.QPushButton("Wrong")
        self.wrongButton.clicked.connect(self.wrong)

        # cancel button
        self.cancelButton = QtGui.QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.cancel)

        self._enable_result_buttons(False)

        # end button
        endButton = QtGui.QPushButton("End")
        endButton.clicked.connect(self.end)

        # button layout
        buttons_box = QtGui.QHBoxLayout()
        buttons_box.addWidget(self.currentPlayerLabel)
        buttons_box.addStretch(1)
        buttons_box.addWidget(self.rightButton)
        buttons_box.addWidget(self.cancelButton)
        buttons_box.addWidget(self.wrongButton)
        buttons_box.addWidget(endButton)

        vbox.addLayout(buttons_box)

    def end(self):
        self._gamewidget.abort_answer()

    def right(self):
        pass

    def wrong(self):
        pass

    def cancel(self):
        self._player_answers(None)

    def keyPressEvent(self, e):
        self.hardware_event(self._game.keyboard, e.key())

    def hardware_event(self, hardware, key):
        if not self._current_player:
            # search for player
            sel_player = None
            for player in self._game.players:
                if player.hardware == hardware and player.key == key:
                    sel_player = player
                    break

            if sel_player:
                self._player_answers(sel_player)

    def _player_answers(self, player):
        self._current_player = player

        # player may be None
        if self._current_player:
            self.currentPlayerLabel.setText(self._current_player.name)
            self._enable_result_buttons(True)
        else:
            self.currentPlayerLabel.setText("")
            self._enable_result_buttons(False)

    def _enable_result_buttons(self, status):
        self.rightButton.setEnabled(status)
        self.wrongButton.setEnabled(status)
        self.cancelButton.setEnabled(status)
