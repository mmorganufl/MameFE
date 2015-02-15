from PyQt5 import QtGui, QtWidgets, QtCore
from mame import TileWidget

class TileRowWidget(QtWidgets.QWidget):
    def __init__(self, startIndex, visibleCount, totalCount, source, filter):
        super(TileRowWidget, self).__init__()
        self._animationDone = True
        self._visibleCount = visibleCount
        self._totalCount = totalCount
        self._source = source
        self._filter = filter
        self._currentIndex = startIndex
        self._source = source
        self._loadRoms()
        
    def _loadRoms(self):
        startIndex = (self._currentIndex - 2) % self._totalCount        
        self._ROMs = self._source.getRoms(self._filter, startIndex, self._visibleCount + 2)
        
    def initialize(self):        
        self._width = self.size().width()
        self._height = self.size().height()
        
        self._tileWidth = int((self._width * .8) / self._visibleCount)
        self._tileHeight = int(((self._tileWidth) * 3 / 4)) # 4 x 3 ratio
        self._tileSpacing = int((self._width * .2) / (self._visibleCount + 1))    
        
        self._label = QtWidgets.QLabel(self)
        self._label.setGeometry(QtCore.QRect(self._tileSpacing, 0, self._width, self._height * .2))
        self._label.setText("<font color='white'>" + str(self._filter) + "</font>");
        self._label.setFont(QtGui.QFont("Arial", .11 * self._height, QtGui.QFont.Bold))
        self._label.setScaledContents(True)
        self._label.setAlignment(QtCore.Qt.AlignTop)        
    
        self._tiles = list()
        for x in range(0, len(self._ROMs)):
            tile = TileWidget.TileWidget(self._ROMs[x].ImagePath())   
            tile.setParent(self)
            tile.setGeometry(QtCore.QRect(self._tileSpacing + (self._tileSpacing + self._tileWidth) * (x-1), self._height * .20, self._tileWidth, self._tileHeight))            
            self._tiles.append(tile)   
            
        self._frame = QtWidgets.QFrame()
        self._frame.setParent(self)
        self._frame.setFrameStyle(QtWidgets.QFrame.Box)        
        self._frame.setGeometry(QtCore.QRect(self._tileSpacing - 6 + (self._tileSpacing + self._tileWidth), self._height * .20 - 6, self._tileWidth + 12, self._tileHeight + 12))
        self._frame.setStyleSheet("QFrame { border: 5px solid white;}") 
        self._frame.hide()       
            
    def paintEvent(self, e):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(palette)         
                     
        QtWidgets.QWidget.paintEvent(self, e)
        
    def showFrame(self, show):
        if (show == True):
            self._frame.show()
        else:
            self._frame.hide()
            
    ###############################
    # Slides moves the tiles
    ###############################
    def slideTiles(self, moveRight):  
        if self._animationDone != True:
            return
          
        if (moveRight):
            self._newGeometry = self._tiles[0].geometry()            
            self._currentIndex -= 1            
        
        if (not moveRight):
            self._newGeometry = self._tiles[-1].geometry()
            self._currentIndex += 1

        self._currentIndex %= self._totalCount
          
        group = QtCore.QParallelAnimationGroup()        
            
        for tileIdx in range(0, len(self._tiles)):            
            animation = QtCore.QPropertyAnimation(self._tiles[tileIdx], "geometry")
            animation.setDuration(100)
            rect = self._tiles[tileIdx].geometry() 
            x, y, x2, y2 = rect.getCoords()        
            animation.setStartValue(rect)
            if (moveRight == True):
                rect.moveRight(x2 + (self._tileWidth + self._tileSpacing))
            else:
                rect.moveRight(x2 - (self._tileWidth + self._tileSpacing))      
            animation.setEndValue(rect)
            group.addAnimation(animation)
        
        self._animationDone = False
        self._moveRight = moveRight
        
        group.start()
        group.finished.connect(self.animationFinished)
        
        self.group = group
         
    #########################################################
    # Signal for when the animation is finished and 
    # another animation can start
    #########################################################
    def animationFinished(self):
        self._animationDone = True
        self._loadRoms()
        if self._moveRight:           
            tile = self._tiles.pop(-1)            
            tile.setGeometry(self._newGeometry)
            tile.setImage(self._ROMs[0].ImagePath())
            self._tiles.insert(0, tile)
                         
        else:            
            tile = self._tiles.pop(0)            
            tile.setGeometry(self._newGeometry)
            tile.setImage(self._ROMs[-1].ImagePath())
            self._tiles.append(tile)   
        
