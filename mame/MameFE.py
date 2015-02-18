import sys
from PyQt5 import QtWidgets
from mame import MainWindow 

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    w = MainWindow.MainWindow()    
    w.showFullScreen()    
    sys.exit(app.exec_())