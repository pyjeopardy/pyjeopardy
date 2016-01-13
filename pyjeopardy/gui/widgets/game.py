from PySide import QtGui

class JeopardyGameWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        self._game = kwargs.pop('game')

        super(JeopardyGameWidget, self).__init__(*args, **kwargs)

        # title
        title = QtGui.QLabel('Yolo')

        # layout
        hbox = QtGui.QVBoxLayout()
        hbox.addWidget(title)

        self.setLayout(hbox)
