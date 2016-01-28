from PyQt5.QtGui import QColor

class Color:
    def __init__(self, name, r, g, b, whitefg=False):
        self.name = name
        self. qt = QColor(r, g, b)
        self.whitefg = whitefg

    def rgb(self):
        r, g, b, a = self.qt.getRgb()
        return (r, g, b)
