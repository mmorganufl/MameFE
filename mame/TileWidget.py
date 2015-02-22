from PyQt5 import QtGui, QtWidgets, QtCore
import os

class TileWidget(QtWidgets.QWidget):
    def __init__(self, parent, imagePath=None, gameName=None):
        super(TileWidget, self).__init__(parent)
        self.setImage(imagePath)
        self._gameName = gameName        
        
    def paintEvent(self, e):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(palette)
    
        p = QtGui.QPainter(self)               
                
        if (self._image is not None):
            size = self.size()
            #size.setHeight(size.height() * .8)
            image = self._image.scaled(size, aspectRatioMode=QtCore.Qt.IgnoreAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)            
            p.drawPixmap(0, 0, image)
            p.setOpacity(1)
        else:           
            p.setPen(QtGui.QColor(255, 255, 255, 255))
            p.setFont(QtGui.QFont('Georgia', 24)) 
            p.drawText(e.rect(), QtCore.Qt.AlignCenter, "NO IMAGE")        
            
        #size = self.size()
        #titleRect = QtCore.QRect(0, size.height() * .8, size.width(), size.height() * .2)
        #p.setPen(QtGui.QColor(192, 192, 255, 255))
        #p.setFont(QtGui.QFont('Georgia', 16))
        #factor = titleRect.width() / p.fontMetrics().width(self._gameName) * .9             
        #f = p.font()
        #f.setPointSizeF(f.pointSizeF()*factor)
        #p.setFont(f)    
        #if p.fontMetrics().height() * .9 > size.height() * .2:
        #    factor = titleRect.height() / p.fontMetrics().height() * .9
        #    f = p.font()
        #    f.setPointSizeF(f.pointSizeF()*factor)  
        #p.setFont(f)      
        #p.drawText(titleRect, QtCore.Qt.AlignCenter, self._gameName)
        QtWidgets.QWidget.paintEvent(self, e)
        p.end()
        
    def setImage(self, imagePath):
        self._image = None
        if (imagePath is not None): 
            self._imagePath = imagePath
            if os.path.isfile(self._imagePath):        
                self._image = QtGui.QPixmap(imagePath)        
        self.update()     
           
