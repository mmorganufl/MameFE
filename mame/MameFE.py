import sys
from PyQt5 import QtWidgets
from mame import RomSelectionWidget 

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    w = RomSelectionWidget.RomSelectionWidget()    
    w.showFullScreen()    
    sys.exit(app.exec_())