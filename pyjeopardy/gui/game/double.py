from PyQt5 import QtCore, QtWidgets

from pyjeopardy.config import FONT_SIZE_DOUBLE, FONT_SIZE_DOUBLE_BET


class JeopardyDoubleWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')
        self._answer = kwargs.pop('answer')
        self._button = kwargs.pop('button')  # not needed here, passed back
        self._game_widget = kwargs.pop('game_widget')

        self._content = None

        super(JeopardyDoubleWidget, self).__init__(*args, **kwargs)

        self._label = QtWidgets.QLabel("Double Jeopardy")
        self._label.setStyleSheet("QLabel {{ font-size: {}px; }}".format(
            FONT_SIZE_DOUBLE))
        self._label.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Fixed)
        self._label.setAlignment(QtCore.Qt.AlignCenter)

        self._listWidget = QtWidgets.QListWidget()
        self._listWidget.itemSelectionChanged.connect(self.update_buttons)

        for player in self._game.players:
            item = QtWidgets.QListWidgetItem(player.name)
            item.setData(QtCore.Qt.UserRole, player)

            self._listWidget.addItem(item)

        self._bet = QtWidgets.QSpinBox()
        self._bet.setMinimum(0.5 * self._answer.get_points())
        self._bet.setMaximum(2 * self._answer.get_points())
        self._bet.setValue(self._answer.get_points())
        self._bet.setSingleStep(50)
        self._bet.setStyleSheet("QSpinBox {{ font-size: {}px; }}".format(
            FONT_SIZE_DOUBLE_BET))

        self._confirmButton = QtWidgets.QPushButton("Go!")
        self._confirmButton.clicked.connect(self.confirm)
        self._confirmButton.setEnabled(False)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self._bet)
        hbox.addWidget(self._listWidget)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self._label)
        vbox.addLayout(hbox)
        vbox.addWidget(self._confirmButton)

        self.setLayout(vbox)

    def confirm(self, event):
        player = self._get_sel_player()
        if not player:
            return

        self._game_widget.open_answer(self._answer, self._button,
                               double_bet=self._bet.value(),
                               double_player=player)

    def update_buttons(self):
        if self._listWidget.selectedItems():
            self._confirmButton.setEnabled(True)
        else:
            self._confirmButton.setEnabled(False)

    def _get_sel_player(self):
        item = self._listWidget.selectedItems()

        if len(item) != 1:
            return  None
        return item[0].data(QtCore.Qt.UserRole)
