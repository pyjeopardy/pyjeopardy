from PyQt5 import QtWidgets

from .answer import JeopardyAnswerWidget
from .double import JeopardyDoubleWidget
from .end import JeopardyEndWidget
from .points import JeopardyPointsWidget

from pyjeopardy.config import FONT_SIZE_ANSWER_POINTS, FONT_SIZE_CATEGORIES, \
    FONT_SIZE_ROUND_NAME, FONT_SIZE_LOG
from pyjeopardy.game import HardwareError

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
        title.setStyleSheet("* {{ font-size: {}px; }}".format(
            FONT_SIZE_ROUND_NAME))

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
            title.setStyleSheet("* {{ font-size: {}px; }}".format(
                FONT_SIZE_CATEGORIES))
            self.answersGrid.addWidget(title, 0, cat_num)

            for answer_num, answer in enumerate(cat.answers):
                tmp = QtWidgets.QPushButton(str(answer.get_points()))

                # resize to full width
                tmp.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Expanding)

                # set font size
                tmp.setStyleSheet("* {{ font-size: {}px; }}".format(
                    FONT_SIZE_ANSWER_POINTS))

                # add event handler
                tmp.clicked.connect(lambda clicked,answer=answer,button=tmp:
                                    self.open_answer(answer, button))

                self.answersGrid.addWidget(tmp, answer_num+1, cat_num)

    def open_answer(self, answer, button, double_bet=None, double_player=None):
        if answer.is_double() and not (double_bet and double_player):
            #TODO: show JeopardyDoubleWidget(game=self._game,
            #                                answer=answer,
            #                                player=TODO)
            # Where can we get the currently answer-selecting player from? Has
            # to be passed to the JeopardyDoubleWidget and JeopardyAnswerWidget
            # has to be adapted to accept a new player= kwarg.
            #
            # We need to store the selection from the JeopardyDoubleWidget
            # somewhere and make sure it is used in the JeopardyAnswerWidget
            # correctly afterwards.
            doublewidget = JeopardyDoubleWidget(game=self._game,
                                                answer=answer,
                                                button=button,
                                                game_widget=self)
            self._main.show_widget(doublewidget)
        else:
            try:
                answerwidget = JeopardyAnswerWidget(answer=answer,
                                                    gamewidget=self,
                                                    game=self._game,
                                                    main=self._main,
                                                    double_bet=double_bet,
                                                    double_player=double_player)
            except HardwareError as e:
                QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                      "Hardware error", str(e)).exec_()
                return

            self._cur_answer = answer
            self._cur_button = button

            self._main.close_double_widget()  # in case it is open
            self._main.show_widget(answerwidget)

    def close_answer(self):
        self._main.close_answer()

        self._game.log.answer_closed(self._cur_answer)

        self.points.update()
        self._disable_button(self._cur_answer, self._cur_button)

        self._cur_answer = None
        self._cur_button = None

        if self._game.log.round_finished():
            endwidget = JeopardyEndWidget(main=self._main, game=self._game)
            self._main.show_widget(endwidget)

    def _disable_button(self, answer, button):
        button.setEnabled(False)

        # update text
        log = self._game.log.get(answer)
        new_label = []
        for entry in log:
            last_player = entry.player

            if entry.points >= 0:
                format_str = "+{} {}"
            elif entry.points < 0:
                format_str = "{} {}"
            new_label.append(format_str.format(entry.points,
                                               entry.player.name))
        button.setText("\n".join(new_label))

        # color
        player = self._game.log.get_winner_of_answer(answer)
        if player:
            bg = player.color.rgb()
            fg = player.color.textcolor_rgb()

            button.setStyleSheet("background-color: rgb({}, {}, {});"
                                 "color: rgb({}, {}, {});"
                                 "font-size: {}px;".format(
                bg[0], bg[1], bg[2], fg[0], fg[1], fg[2], FONT_SIZE_LOG))
        else:
            button.setStyleSheet("font-size: {}px;".format(FONT_SIZE_LOG))
