from PyQt5 import QtGui, QtWidgets, QtCore

class TileWidget(QtWidgets.QWidget):
    def __init__(self, imagePath=None):
        super(TileWidget, self).__init__()
        self.setImage(imagePath)
        
    def paintEvent(self, e):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(palette)
        
        p = QtGui.QPainter(self)
        if (self._image is not None):
            image = self._image.scaled(self.size(), aspectRatioMode=QtCore.Qt.IgnoreAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)            
            p.drawPixmap(0, 0, image)
            
        QtWidgets.QWidget.paintEvent(self, e)
        
    def setImage(self, imagePath):
        if (imagePath is not None):
            self._image = QtGui.QPixmap(imagePath)
        else:
            self._image = None
        self.update()