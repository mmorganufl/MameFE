from PyQt5 import QtGui, QtWidgets, QtCore


class TileWidget(QtWidgets.QWidget):
    def __init__(self, parent, imagePath=None):
        super(TileWidget, self).__init__(parent)
        self.setImage(imagePath)        
        
    def paintEvent(self, e):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(palette)
                
        if (self._image is not None):
            image = self._image.scaled(self.size(), aspectRatioMode=QtCore.Qt.IgnoreAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)            
            print("tile height: %d" % self.size().height())
            p = QtGui.QPainter(self)            
            p.drawPixmap(0, 0, image)
            
        QtWidgets.QWidget.paintEvent(self, e)
        
    def setImage(self, imagePath):
        if (imagePath is not None):
            self._imagePath = imagePath
            self._image = QtGui.QPixmap(imagePath)
        else:
            self._image = None
        self.update()     
           
