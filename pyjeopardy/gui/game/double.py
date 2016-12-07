from PyQt5 import QtWidgets

from pyjeopardy.config import FONT_SIZE_CUR_PLAYERS


class JeopardyDoubleWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')
        self._answer = kwargs.pop('answer')
        self._player = kwargs.pop('player')

        self._content = None

        super(JeopardyDoubleWidget, self).__init__(*args, **kwargs)

        vbox = QtWidgets.QVBoxLayout()

        self._label = QtWidgets.QLabel("Double Jeopardy")

        self._name = QtWidgets.QLabel(self._player.name)
        self._name.setAutoFillBackground(True)
        p = self._name.palette()
        p.setColor(self._name.backgroundRole(), self._player.color.qt)
        p.setColor(self._name.foregroundRole(), self._player.color.textcolor())
        self._name.setPalette(p)
        self._name.setStyleSheet("QWidget {{ font-size: {}px; }}".format(
            FONT_SIZE_PLAYERS))

        self._bet = QtWidgets.QSpinBox()
        self._bet.setMaximum(2 * self._answer.get_points())
        self._bet.setValue(self._answer.get_points())
        self._bet.setSingleStep(50)
        self._editingFinished.connect(self.confirm)
        #TODO: focus the spinbox?

        vbox.addWidget(self._label)
        vbox.addWidget(self._name)
        vbox.addWidget(self._bet)

        self.setLayout(vbox)

    def confirm(self, event):
        #TODO: close widget and return self._bet.value()
        pass
