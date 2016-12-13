from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class Color:
    def __init__(self, name, r, g, b, whitefg=False):
        self.name = name
        self.qt = QColor(r, g, b)
        self.whitefg = whitefg

    def rgb(self):
        r, g, b, a = self.qt.getRgb()
        return (r, g, b)

    def textcolor(self):
        if self.whitefg:
            return QColor(Qt.white)
        return QColor(Qt.black)

    def textcolor_rgb(self):
        r, g, b, a = self.textcolor().getRgb()
        return (r, g, b)
