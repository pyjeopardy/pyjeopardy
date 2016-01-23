from PySide import QtGui

from pyjeopardy.game import Round, ParserError

class JeopardyRoundsWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')
        self._main = kwargs.pop('main')

        super(JeopardyRoundsWidget, self).__init__(*args, **kwargs)

        # list
        self.listWidget = QtGui.QListWidget(self)
        self.listWidget.currentItemChanged.connect(self.round_changed)

        # title
        title = QtGui.QLabel('Rounds')

        # add button
        addButton = QtGui.QPushButton("Add")
        addButton.clicked.connect(self.add_round)

        # layout
        hbox = QtGui.QVBoxLayout()
        hbox.addWidget(title)
        hbox.addWidget(self.listWidget)
        hbox.addWidget(addButton)

        self.setLayout(hbox)

        self.update()

    def update(self):
        self.listWidget.clear()

        for round in self._game.rounds:
            self.listWidget.addItem(QtGui.QListWidgetItem(round.name))

    def add_round(self):
        fname, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
            filter='JSON files (*.json);;All files (*)')

        if fname:
            round = Round()
            try:
                round.load(fname)
            except ParserError as e:
                errorBox = QtGui.QMessageBox(QtGui.QMessageBox.Critical,
                    "Error loading round", "Cannot load JSON file")
                errorBox.setInformativeText(e.value)
                errorBox.exec_()
                return

            self._game.add_round(round)

            self.update()

            # select newly added item
            self.listWidget.setCurrentRow(self.listWidget.count()-1)

    def round_changed(self):
        self.parent().update_play_status()

    def get_selected_round(self):
        if not self.listWidget.currentItem():
            return None

        pos = self.listWidget.currentRow()

        if pos >= len(self._game.rounds):
            return None

        return self._game.rounds[pos]