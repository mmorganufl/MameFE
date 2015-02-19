from PyQt5 import QtGui, QtWidgets, QtCore
from mame import TileWidget

class TileRowWidget(QtWidgets.QWidget):
    def __init__(self, parent, startIndex, visibleCount, totalCount, source, filter):        
        super(TileRowWidget, self).__init__(parent)        
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
     
    def GetSelectedRom(self):
        return self._ROMs[2]
       
    def initialize(self):
        LABEL_PERCENTAGE = .2
        TILE_HEIGHT_PERCENTAGE = 1 - LABEL_PERCENTAGE
        TILE_WIDTH_PERCENTAGE = .8
        TILE_SPACE_PERCENTAGE = 1 - TILE_WIDTH_PERCENTAGE
        
        self._width = self.size().width()
        self._height = self.size().height()
                
        self._tileWidth = int((self._width * TILE_WIDTH_PERCENTAGE) / self._visibleCount)
        self._tileHeight = self._height * TILE_HEIGHT_PERCENTAGE
        self._tileSpacing = int((self._width * TILE_SPACE_PERCENTAGE) / (self._visibleCount + 1))    
        
        self._label = QtWidgets.QLabel(self)
        self._label.setGeometry(QtCore.QRect(self._tileSpacing, 0, self._width, self._height * LABEL_PERCENTAGE))
        self._label.setText("<font color='white'>" + str(self._filter) + "</font>");
        self._label.setFont(QtGui.QFont("Helvetica", .11 * self._height, QtGui.QFont.Bold))
        self._label.setScaledContents(True)
        self._label.setAlignment(QtCore.Qt.AlignTop)        
    
        self._tiles = list()
        for i in range(0, len(self._ROMs)):
            tile = TileWidget.TileWidget(self, self._ROMs[i].ImagePath())   
            tile.setParent(self)            
            x = self._tileSpacing + (self._tileSpacing + self._tileWidth) * (i-1)
            y = self._height * LABEL_PERCENTAGE  # Lowered to make room for the label
                    
            tile.setGeometry(QtCore.QRect(x, y, self._tileWidth, self._tileHeight))                        
            self._tiles.append(tile)   
            
        self._frame = QtWidgets.QFrame()
        self._frame.setParent(self)
        self._frame.setFrameStyle(QtWidgets.QFrame.Box)
        
        FRAME_WIDTH = 5
        centerTileIdx = int(self._visibleCount / 2)
        print("center tile idx: %d" % centerTileIdx)
        x = self._tileSpacing - FRAME_WIDTH + ((self._tileSpacing + self._tileWidth) * centerTileIdx)
        y = self._height * LABEL_PERCENTAGE - FRAME_WIDTH
        
        self._frame.setGeometry(QtCore.QRect(x, y, self._tileWidth + (FRAME_WIDTH * 2), self._tileHeight + FRAME_WIDTH))
        self._frame.setStyleSheet("QFrame { border: 5px solid white;}") 
        self._frame.hide()       
            
    def paintEvent(self, e):
        QtWidgets.QWidget.paintEvent(self, e)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(palette)          
        
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
        self.group = group
        group.finished.connect(self.animationFinished)       
        
         
    #########################################################
    # Signal for when the animation is finished and 
    # another animation can start
    #########################################################
    def animationFinished(self):
        self._animationDone = True
        self._loadRoms()
        if self._moveRight:           
            self._tiles.pop(-1)
            tile = TileWidget.TileWidget(self, self._ROMs[0].ImagePath())  
            tile.setParent(self)       
            tile.setGeometry(self._newGeometry)            
            self._tiles.insert(0, tile)
                         
        else:            
            self._tiles.pop(0)
            tile = TileWidget.TileWidget(self, self._ROMs[-1].ImagePath())  
            tile.setParent(self)           
            tile.setGeometry(self._newGeometry)            
            self._tiles.append(tile)   
                
        tile.show()
