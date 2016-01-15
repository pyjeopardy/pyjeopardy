from PySide import QtGui

class JeopardyGameWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')
        self._round = kwargs.pop('round')

        super(JeopardyGameWidget, self).__init__(*args, **kwargs)

        # title
        title = QtGui.QLabel(self._round.name)

        # grid with answers
        self.answersGrid = QtGui.QGridLayout()
        self._draw_grid()

        # layout
        hbox = QtGui.QVBoxLayout()
        hbox.addWidget(title)
        hbox.addLayout(self.answersGrid)

        self.setLayout(hbox)

    def _draw_grid(self):
        for cat_num,cat in enumerate(self._round.categories):
            title = QtGui.QLabel(cat.name)
            self.answersGrid.addWidget(title, 0, cat_num)

            for answer_num,answer in enumerate(cat.answers):
                tmp = QtGui.QPushButton(str(answer.get_points()))
                self.answersGrid.addWidget(tmp, answer_num+1, cat_num)
