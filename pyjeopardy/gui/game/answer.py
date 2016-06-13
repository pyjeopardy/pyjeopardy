from PyQt5 import QtCore, QtWidgets

from pyjeopardy.config import FONT_SIZE_ANSWER, FONT_SIZE_CUR_PLAYER, \
    AUDIO_WAITING

from .image import ImageWidget


class JeopardyAnswerWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')
        self._gamewidget = kwargs.pop('gamewidget')
        self._answer = kwargs.pop('answer')
        self._main = kwargs.pop('main')

        self._current_player = None
        self._content = None

        super(JeopardyAnswerWidget, self).__init__(*args, **kwargs)

        # layout
        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        # content
        if self._answer.is_text():
            self._content = QtWidgets.QLabel(self._answer.get_text())
            self._content.setStyleSheet("QLabel {{ font-size: {}px; }}".format(
                FONT_SIZE_ANSWER))
            self._content.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Expanding)
            self._content.setWordWrap(True)
        elif self._answer.is_image():
            self._content = ImageWidget(filename=self._answer.get_path())
            self._content.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Expanding)
        elif self._answer.is_audio():
            self._content = QtWidgets.QPushButton("Stop")
            self._content.clicked.connect(self._audio_toggle)
        # <- add further types here

        if self._content:
            vbox.addWidget(self._content, alignment=QtCore.Qt.AlignCenter)
        else:
            print("ERROR: unsupported answer type")

        # current player
        self.currentPlayerLabel = QtWidgets.QLabel("")
        self.currentPlayerLabel.setStyleSheet("QLabel {{ font-size: "
                                              "{}px; }}".format(
                                                FONT_SIZE_CUR_PLAYER))

        # right button
        self.rightButton = QtWidgets.QPushButton("Right")
        self.rightButton.clicked.connect(self.right)

        # wrong button
        self.wrongButton = QtWidgets.QPushButton("Wrong")
        self.wrongButton.clicked.connect(self.wrong)

        # cancel button
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.cancel)

        self._enable_result_buttons(False)

        # end button
        endButton = QtWidgets.QPushButton("End")
        endButton.clicked.connect(self.end)

        # button layout
        buttons_box = QtWidgets.QHBoxLayout()
        buttons_box.addWidget(self.currentPlayerLabel)
        buttons_box.addStretch(1)
        buttons_box.addWidget(self.rightButton)
        buttons_box.addWidget(self.cancelButton)
        buttons_box.addWidget(self.wrongButton)
        buttons_box.addWidget(endButton)

        vbox.addLayout(buttons_box)

        # play waiting music
        if self._answer.is_audio():
            self._main.audio_play(self._answer.get_path())
        else:
            self._main.audio_play(AUDIO_WAITING)

        # start hardware
        self._game.start_hardware(self.hardware_event)

    def hideEvent(self, event):
        self._audio_stop()
        self._game.stop_hardware()

        super(JeopardyAnswerWidget, self).hideEvent(event)

    def end(self):
        self._gamewidget.close_answer()

    def right(self):
        self._update_points(self._answer.get_points())
        self._gamewidget.close_answer()

    def wrong(self):
        self._update_points(-1 * self._answer.get_points())
        self._player_answers(None)
        self._game.start_hardware(self.hardware_event)

    def cancel(self):
        self._update_points(0)
        self._player_answers(None)
        self._game.start_hardware(self.hardware_event)

    def _update_points(self, points):
        self._current_player.add_points(points)
        self._game.log.add(self._answer, self._current_player, points)

    def keyPressEvent(self, e):
        if self._game.keyboard.active:
            self.hardware_event(self._game.keyboard, e.key())

    def hardware_event(self, hardware, key):
        self._game.stop_hardware()

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

            self._audio_stop()
        else:
            self.currentPlayerLabel.setText("")
            self._enable_result_buttons(False)

    def _enable_result_buttons(self, status):
        self.rightButton.setEnabled(status)
        self.wrongButton.setEnabled(status)
        self.cancelButton.setEnabled(status)

    def _audio_play(self):
        self._main.audio_play()

        if self._answer.is_audio():
            self._content.setText("Stop")

    def _audio_stop(self):
        self._main.audio_stop()

        if self._answer.is_audio():
            self._content.setText("Start")

    def _audio_toggle(self):
        if self._main.audio_playing():
            self._audio_stop()
        else:
            self._audio_play()
