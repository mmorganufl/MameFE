#!/usr/bin/python3
import sys
from PyQt4 import QtGui, QtCore
import RomSelectionWidget 

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    w = RomSelectionWidget.RomSelectionWidget()        
    w.showFullScreen()        
    #w.show()
    #w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint);
    #w.setWindowState(w.windowState() ^ QtCore.Qt.Window)
    w.InitializeScreen()
    sys.exit(app.exec_())
