from PyQt5 import QtWidgets

from .answer import JeopardyAnswerWidget
from .points import JeopardyPointsWidget

class JeopardyGameWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')
        self._main = kwargs.pop('main')
        self._round = kwargs.pop('round')

        self._cur_answer = None
        self._cur_button = None

        super(JeopardyGameWidget, self).__init__(*args, **kwargs)

        # title
        title = QtWidgets.QLabel(self._round.name)

        # grid with answers
        self.answersGrid = QtWidgets.QGridLayout()
        self._draw_grid()

        # players with points
        self.points = JeopardyPointsWidget(game=self._game)

        # layout
        hbox = QtWidgets.QVBoxLayout()
        hbox.addWidget(title)
        hbox.addLayout(self.answersGrid)
        hbox.addWidget(self.points)

        self.setLayout(hbox)

    def _draw_grid(self):
        for cat_num, cat in enumerate(self._round.categories):
            title = QtWidgets.QLabel(cat.name)
            self.answersGrid.addWidget(title, 0, cat_num)

            for answer_num, answer in enumerate(cat.answers):
                tmp = QtWidgets.QPushButton(str(answer.get_points()))

                # resize to full width
                tmp.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Expanding)

                # add event handler
                tmp.clicked.connect(lambda clicked,answer=answer,button=tmp:
                                    self.open_answer(answer, button))

                self.answersGrid.addWidget(tmp, answer_num+1, cat_num)

    def open_answer(self, answer, button):
        self._cur_answer = answer
        self._cur_button = button

        answerwidget = JeopardyAnswerWidget(answer=answer, gamewidget=self,
                                            game=self._game)
        self._main.show_answer(answerwidget)

    def close_answer(self):
        self._main.close_answer()

        self.points.update()
        self._disable_button(self._cur_answer, self._cur_button)

        self._cur_answer = None
        self._cur_button = None

    def _disable_button(self, answer, button):
        button.setEnabled(False)

        # update text
        log = self._game.log.get(answer)
        new_label = []
        for entry in log:
            if entry.points >= 0:
                format_str = "+{} {}"
            elif entry.points < 0:
                format_str = "-{} {}"
            new_label.append(format_str.format(entry.points,
                                               entry.player.name))
        button.setText("\n".join(new_label))
