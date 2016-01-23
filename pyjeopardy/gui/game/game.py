from PySide import QtGui

from .answer import JeopardyAnswerWidget
from .points import JeopardyPointsWidget

class JeopardyGameWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')
        self._main = kwargs.pop('main')
        self._round = kwargs.pop('round')

        super(JeopardyGameWidget, self).__init__(*args, **kwargs)

        # title
        title = QtGui.QLabel(self._round.name)

        # grid with answers
        self.answersGrid = QtGui.QGridLayout()
        self._draw_grid()

        # players with points
        self.points = JeopardyPointsWidget(game=self._game)

        # layout
        hbox = QtGui.QVBoxLayout()
        hbox.addWidget(title)
        hbox.addLayout(self.answersGrid)
        hbox.addWidget(self.points)

        self.setLayout(hbox)

    def _draw_grid(self):
        for cat_num, cat in enumerate(self._round.categories):
            title = QtGui.QLabel(cat.name)
            self.answersGrid.addWidget(title, 0, cat_num)

            for answer_num, answer in enumerate(cat.answers):
                tmp = QtGui.QPushButton(str(answer.get_points()))

                # resize to full width
                tmp.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                  QtGui.QSizePolicy.Expanding)

                # add event handler
                tmp.clicked.connect(lambda answer=answer:
                                    self.open_answer(answer))

                self.answersGrid.addWidget(tmp, answer_num+1, cat_num)

    def open_answer(self, answer):
        answerwidget = JeopardyAnswerWidget(answer=answer, gamewidget=self,
                                            game=self._game)
        self._main.show_answer(answerwidget)

    def abort_answer(self):
        self._main.close_answer()
