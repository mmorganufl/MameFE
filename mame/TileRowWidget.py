from PyQt4 import QtGui, QtCore
import TileWidget

class TileRowWidget(QtGui.QWidget):
    def __init__(self, parent, startIndex, visibleCount, totalCount, source, filter):        
        super(TileRowWidget, self).__init__(parent)
        
        self._currentIndex  = startIndex  
        self._visibleCount  = visibleCount
        self._totalRomCount = totalCount
        self._romSource     = source
        self._filter        = filter        
        self._animationDone = True
                
        self.LoadRoms()
        
    def LoadRoms(self):
        startIndex = (self._currentIndex - 2) % self._totalRomCount        
        self._ROMs = self._romSource.getRoms(self._filter, startIndex, self._visibleCount + 2)
        self._selectedRom = self._ROMs[int(self._visibleCount / 2) + 1] # visible count must be odd
     
    def GetSelectedRom(self):
        return self._selectedRom
       
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
        
        self._label = QtGui.QLabel(self)
        self._label.setGeometry(QtCore.QRect(self._tileSpacing, 0, self._width * .5, self._height * LABEL_PERCENTAGE))
        self._label.setText("<font color='white'>" + str(self._filter) + "</font>");
        self._label.setFont(QtGui.QFont("DejaVu Sans", .11 * self._height, QtGui.QFont.Bold))
        self._label.setScaledContents(True)
        self._label.setAlignment(QtCore.Qt.AlignTop)        
    
        self._countLabel = QtGui.QLabel(self)
        self._countLabel.setGeometry(QtCore.QRect(self._width * .5, 0, self._width * .5 - self._tileSpacing, self._height * LABEL_PERCENTAGE))
        self._countLabel.setFont(QtGui.QFont("Arial", .07 * self._height))
        self._countLabel.setScaledContents(True)
        self._countLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self._countLabel.hide()
        
        self._tiles = list()
        for i in range(0, len(self._ROMs)):
            tile = TileWidget.TileWidget(self, self._ROMs[i].ImagePath(), self._ROMs[i].GameName())   
            tile.setParent(self)            
            x = self._tileSpacing + (self._tileSpacing + self._tileWidth) * (i-1)
            y = self._height * LABEL_PERCENTAGE  # Lowered to make room for the label
                    
            tile.setGeometry(QtCore.QRect(x, y, self._tileWidth, self._tileHeight))                        
            self._tiles.append(tile)   
           
        
        self._frame = QtGui.QFrame()        
        self._frame.setParent(self)
        self._frame.setFrameShape(QtGui.QFrame.StyledPanel)
        
        FRAME_WIDTH = 5
        
        centerTileIdx = int(self._visibleCount / 2)
        print("center tile idx: %d" % centerTileIdx)
        x = self._tileSpacing - FRAME_WIDTH + ((self._tileSpacing + self._tileWidth) * centerTileIdx)
        y = self._height * LABEL_PERCENTAGE - FRAME_WIDTH
        
        self._frame.setGeometry(QtCore.QRect(x, y, self._tileWidth + (FRAME_WIDTH * 2), self._tileHeight + FRAME_WIDTH))
        self._frame.setStyleSheet("QFrame { border: 3px solid white;}") 
        self._frame.hide()       
            
    def paintEvent(self, e):
        QtGui.QWidget.paintEvent(self, e)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(palette)          
        
    def showFrame(self, show):
        if (show == True):
            self._frame.show()      
            self.updateCountLabel()                  
        else:
            self._frame.hide()
            self._countLabel.hide()
                        
    def updateCountLabel(self):
        indexStr = "<font color='white'>" + str(self._currentIndex % self._totalRomCount + 1)
        self._countLabel.setText(indexStr + " | " + str(self._totalRomCount)) 
        self._countLabel.show()
        
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

        self._currentIndex %= self._totalRomCount
          
        group = QtCore.QParallelAnimationGroup()        
            
        for tileIdx in range(0, len(self._tiles)):            
            animation = QtCore.QPropertyAnimation(self._tiles[tileIdx], "geometry")
            animation.setDuration(350)
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
        self.updateCountLabel()       
        
         
    #########################################################
    # Signal for when the animation is finished and 
    # another animation can start
    #########################################################
    def animationFinished(self):
        self._animationDone = True        
        self.LoadRoms()
        if self._moveRight:           
            self._tiles.pop(-1)
            tile = TileWidget.TileWidget(self, self._ROMs[0].ImagePath(), self._ROMs[0].GameName())  
            tile.setParent(self)       
            tile.setGeometry(self._newGeometry)            
            self._tiles.insert(0, tile)
            
                         
        else:            
            self._tiles.pop(0)
            tile = TileWidget.TileWidget(self, self._ROMs[-1].ImagePath(), self._ROMs[-1].GameName())
            tile.setParent(self)           
            tile.setGeometry(self._newGeometry)            
            self._tiles.append(tile)  
                        
        tile.show()
        
