#!/usr/bin/python3
 
# Import PySide classes
import sys
from PySide import QtGui

from pyjeopardy.gui import JeopardyMain

def main():
    app = QtGui.QApplication(sys.argv)
    main = JeopardyMain()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
