from PySide import QtGui

class JeopardyAnswerWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')
        self._main = kwargs.pop('main')
        self._answer = kwargs.pop('answer')

        super(JeopardyAnswerWidget, self).__init__(*args, **kwargs)

        # layout
        hbox = QtGui.QVBoxLayout()
        self.setLayout(hbox)

        # content
        if self._answer.is_text():
            text = QtGui.QLabel(self._answer.get_text())
            hbox.addWidget(text)
        else:
            print("ERROR: unsupported answer type")
