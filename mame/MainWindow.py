from PyQt5 import QtCore, QtWidgets, QtGui
from mame.TileRowWidget import TileRowWidget
from mame.RomSource import GenreRomSource
from mame.Configuration import Configuration

class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
    
        # State variables
        self._selectedRow = 0    
        self._animationDone = True
        self._rows = list()
        self._rowSelection = dict()
        
        # Set up initial window
        self.setGeometry(QtCore.QRect(100, 100, 1024, 768))
        
        # Get the window dimensions
        height = self.size().height()
        width = self.size().width()
        
        # Set up the row dimensions
        # 11 + 2(rows) * 37 + 3(spaces) * 5 = 100
        bannerHeight = int(height * .11)
        self._rowHeight = int(height * .37)
        self._rowSpacing = int(height * .05)
        
        # Set the background color to gray-blue
        p = self.palette()        
        p.setColor(self.backgroundRole(), QtGui.QColor(80, 80, 100))
        self.setPalette(p)
            
        # Create the banner
        self._bannerLabel = QtWidgets.QLabel(self)
        self._bannerLabel.setGeometry(QtCore.QRect(0, 0, width, bannerHeight))
        self._bannerLabel.setAutoFillBackground(True)
        self._bannerLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        
        # Set the background of the banner to black
        bp = self._bannerLabel.palette()
        bp.setColor(self._bannerLabel.backgroundRole(), QtGui.QColor(0, 0, 0))
        self._bannerLabel.setPalette(bp)
        
        # Set the banner image
        self._bannerImage = QtGui.QPixmap("images/marquee2.jpg").scaledToHeight(bannerHeight, mode=QtCore.Qt.SmoothTransformation)
        self._bannerLabel.setPixmap(self._bannerImage)
        
        self._config = Configuration("mamefe.ini");
        self._romSource = GenreRomSource(self._config)
        self._numRows = self._romSource.getNumRows(); 
        
               
        self._headers = self._romSource.getHeaders(0, 3)
        topCount = self._romSource.getNumRoms(self._headers[0])        
        # Create the first two rows
        topRow = TileRowWidget(2, 3, topCount, self._romSource, self._headers[0])
        topRow.setGeometry(QtCore.QRect(0, bannerHeight + self._rowSpacing, width, self._rowHeight))
        topRow.setParent(self)
        topRow.initialize()
        
        secondCount = self._romSource.getNumRoms(self._headers[1])    
        secondRow = TileRowWidget(1, 3, secondCount, self._romSource, self._headers[1])
        secondRow.setGeometry(QtCore.QRect(0, bannerHeight + self._rowSpacing * 2 + self._rowHeight, width, self._rowHeight))
        secondRow.setParent(self)
        secondRow.initialize()        
        
        topRow.showFrame(True)
        secondRow.showFrame(False)
        
        topRow.lower()
        secondRow.lower()
        self._bannerLabel.raise_()
        
        self._rows.append(topRow)
        self._rows.append(secondRow)               
   
    def keyPressEvent(self, e):
        key = e.key()  
        if (key == QtCore.Qt.Key_Left):      
            self._rows[self._selectedRow].slideTiles(True)
            
        elif (key == QtCore.Qt.Key_Right):
            self._rows[self._selectedRow].slideTiles(False) 
            
        elif (key == QtCore.Qt.Key_Down):
            if (self._selectedRow > 0):
                self._rows[self._selectedRow].showFrame(False)
                self.slideRow(True)
                self._selectedRow -= 1
                self._rows[self._selectedRow].showFrame(True)
            
        elif (key == QtCore.Qt.Key_Up):
            if (self._selectedRow < (len(self._rows) - 1)):
                self._rows[self._selectedRow].showFrame(False)            
                self._selectedRow += 1
                self.slideRow(False)                  
                self._rows[self._selectedRow].showFrame(True)
      
    ########################################################
    # Slides moves the tiles
    # @param moveDown - Set True to slide the rows down
    ########################################################
    def slideRow(self, moveDown):  
        if self._animationDone != True:
            return
          
        group = QtCore.QParallelAnimationGroup()
                
        for row in self._rows:
            animation = QtCore.QPropertyAnimation(row, "geometry")
            animation.setDuration(100)
            rect = row.geometry() 
            x, y, x2, y2 = rect.getCoords()            
            height = y2-y     
               
            animation.setStartValue(rect)
            if (moveDown == True):
                rect.moveTop(y + (height + self._rowSpacing))
            else:
                rect.moveTop(y - (height + self._rowSpacing))
                      
            animation.setEndValue(rect)
            group.addAnimation(animation)
        
        self._animationDone = False
        group.start()
        group.finished.connect(self.animationFinished)
        
        self.group = group

    #########################################################
    # Signal for when the animation is finished and 
    # another animation can start
    #########################################################
    def animationFinished(self):
        self._animationDone = True
        
               
