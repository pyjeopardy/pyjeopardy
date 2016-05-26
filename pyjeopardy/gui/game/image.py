from PyQt5 import QtWidgets, QtCore, QtGui


class ImageWidget(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        self.filename = kwargs.pop("filename")

        super(ImageWidget, self).__init__(*args, **kwargs)

        self.pixmap = QtGui.QPixmap(self.filename)

    def sizeHint(self):
        return self.pixmap.size()

    def resizeEvent(self, event):
        super(ImageWidget, self).resizeEvent(event)

        self.setPixmap(self.pixmap.scaled(self.size(),
                       QtCore.Qt.KeepAspectRatio))
