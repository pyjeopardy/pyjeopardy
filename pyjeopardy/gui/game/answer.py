from PySide import QtGui, QtCore

from pyjeopardy.config import ANSWER_FONT_SIZE


class JeopardyAnswerWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        self._gamewidget = kwargs.pop('gamewidget')
        self._answer = kwargs.pop('answer')

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

        # abort button
        abortButton = QtGui.QPushButton("Abort")
        abortButton.clicked.connect(self.abort)

        # button layout
        buttons_box = QtGui.QHBoxLayout()
        buttons_box.addStretch(1)
        buttons_box.addWidget(abortButton)

        vbox.addLayout(buttons_box)

    def abort(self):
        self._gamewidget.abort_answer()
