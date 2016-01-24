#!/usr/bin/python3

# Import PyQt5 classes
import sys
from PyQt5 import QtWidgets

from pyjeopardy.gui import JeopardyMain

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = JeopardyMain()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
