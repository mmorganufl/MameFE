from PyQt5 import QtCore, QtWidgets, QtGui
from mame.TileRowWidget import TileRowWidget
from mame.RomSource import GenreRomSource
from mame.Configuration import Configuration
import sys

class MainWindow(QtWidgets.QWidget):
    """ The main window of the front end. """
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
    
        # State variables
        self._selectedRow   = 0    
        self._animationDone = True
        self._rows          = list()
        self._totalNumRows  = 0
        self._rowSelection  = dict()
        self._config        = Configuration("mamefe.ini");
        self._romSource     = GenreRomSource(self._config)        
        
    def showFullScreen(self):
        QtWidgets.QWidget.showFullScreen(self)
        # Set up initial window
        #self.setGeometry(QtCore.QRect(100, 100, 1024, 768))        
        
        # Get the window dimensions
        height = self.size().height()
        width = self.size().width()
        
        if (width * 3) == (height * 4):  # a 4:3 display            
            self._numColsToDisplay = 3
            self._totalNumRowsToDisplay = 2
        else: # assume widescreen, 16:9
            self._numColsToDisplay = 5
            self._totalNumRowsToDisplay = 3 
            
        # Set up the row dimensions
        # The banner will take the upper 10% of the screen
        bannerHeight = int(height * .10)
        
        # The spaces between each row will each take 5% of the screen
        # There will be n+1 row spaces 
        self._rowSpacing = int(height * .05)
        
        # The remaining real estate is divided among the rows
        self._rowHeight = (int(height * ((1 - .05 * (self._totalNumRowsToDisplay + 2)) / self._totalNumRowsToDisplay)))        
        
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
        self._bannerLabel.show()
        
        self._totalNumRows = self._romSource.getNumRows();         
              
        self._headers = self._romSource.getHeaders(0, -1)        
        numRows = min(4, self._totalNumRows)
                
        for i in range(0, numRows):
            count = self._romSource.getNumRoms(self._headers[(i-1) % self._totalNumRows])
            row = TileRowWidget(self, 1, 3, count, self._romSource, self._headers[(i-1) % self._totalNumRows])
            row.setGeometry(QtCore.QRect(0, bannerHeight + self._rowSpacing * (i-1) + self._rowHeight * (i-1), width, self._rowHeight))
            row.setParent(self)
            row.initialize()
            row.showFrame(i == 1)
            row.lower()
            self._rows.append(row)
            row.show()
        self._bannerLabel.raise_()                       
   
    def keyPressEvent(self, e):
        key = e.key()  
        if (key == QtCore.Qt.Key_Left):      
            self._rows[1].slideTiles(True)
            
        elif (key == QtCore.Qt.Key_Right):
            self._rows[1].slideTiles(False) 
            
        elif (key == QtCore.Qt.Key_Down):            
            self._selectedRow -= 1
            self.slideRow(True)          
            
        elif (key == QtCore.Qt.Key_Up):                                        
            self._selectedRow += 1
            self.slideRow(False)                  
                
        elif (key == QtCore.Qt.Key_Escape):
            sys.exit(0)            
            
            
    ########################################################
    # Slides moves the tiles
    # @param moveDown - Set True to slide the rows down
    ########################################################
    def slideRow(self, moveDown):  
        if self._animationDone != True:
            return
          
        self._moveDown = moveDown 
        
        if moveDown:
            self._newGeometry = self._rows[0].geometry()  
        else:
            self._newGeometry = self._rows[-1].geometry()
                                        
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
        group.finished.connect(self.animationFinished)        
        group.start()
        
        self.group = group
               
        
        self._rows[1].showFrame(False)        
        if self._moveDown:
            self._rows.pop(-1)
            count = self._romSource.getNumRoms(self._headers[(self._selectedRow-1)  % self._totalNumRows])                
            row = TileRowWidget(self, 1, 3, count, self._romSource, self._headers[(self._selectedRow-1) % self._totalNumRows])
            row.setGeometry(self._newGeometry)
            row.setParent(self)
            row.initialize()                        
            self._rows.insert(0, row)            
        else:            
            self._rows.pop(0)            
            count = self._romSource.getNumRoms(self._headers[(self._selectedRow+3) % self._totalNumRows])
            row = TileRowWidget(self, 1, 3, count, self._romSource, self._headers[(self._selectedRow+3) % self._totalNumRows])
            row.setGeometry(self._newGeometry)            
            row.setParent(self)            
            row.initialize()           
             
            self._rows.append(row)
            
        row.show()
        row.lower()
        self.repaint()
            
        self._rows[1].showFrame(True)
        

    #########################################################
    # Signal for when the animation is finished and 
    # another animation can start
    #########################################################
    def animationFinished(self):
        self._animationDone = True
        

                
