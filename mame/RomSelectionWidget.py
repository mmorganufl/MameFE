from PyQt4 import QtCore, QtGui
from TileRowWidget import TileRowWidget
from RomSource import RomSource
from Configuration import Configuration
import sys

class RomSelectionWidget(QtGui.QWidget):
    """ The main window of the front end. """
    def __init__(self):
        QtGui.QWidget.__init__(self)
    
        # State variables
        self._selectedRow   = 0
        self._rows          = list()
        self._totalNumRows  = 0
        self._rowSelection  = dict()
        self._config        = Configuration("mamefe.ini");
        self._romSources     = list()
        
        RomSource.init(self._config)
        self._romSources.append(RomSource("genre"))
        self._romSources.append(RomSource("year"))
        self._romSources.append(RomSource("developer"))        
        self._romSourceIndex = 0
        self._animationDone = True
          
        self._romSource = self._romSources[self._romSourceIndex]
        self._romSource.validateDatabase()            
        
        
    def showFullScreen(self):
        QtGui.QWidget.showFullScreen(self)
        # Set up initial window
        #self.setGeometry(QtCore.QRect(0, 0, 1024, 768))        
        #self.setGeometry(QtCore.QRect(0, 0, QtGui.QApplication.desktop().size().width(), QtGui.QApplication.desktop().size().height()))
        self.setGeometry(QtGui.QApplication.desktop().screenGeometry(0))
        self.InitializeScreen()
    
    def InitializeScreen(self):
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
        BANNER_HEIGHT_PERCENTAGE = .1
        self._bannerHeight = int(height * BANNER_HEIGHT_PERCENTAGE)
        
        # The spaces between each row will each take 5% of the screen
        # There will be n+1 row spaces 
        ROW_HEIGHT_PERCENTAGE = 0.05
        self._rowSpacing = int(height * ROW_HEIGHT_PERCENTAGE)
        
        # The remaining real estate is divided among the rows
        self._rowHeight = (int(height * ((1 - ROW_HEIGHT_PERCENTAGE * (self._totalNumRowsToDisplay + 2)) / self._totalNumRowsToDisplay)))        
        
        # Set the background color to gray-blue
        p = self.palette()        
        #p.setColor(self.backgroundRole(), QtGui.QColor(80, 80, 100))
        gradient = QtGui.QLinearGradient(self.size().width()/2, 0, self.size().width()/2, self.size().height())
        gradient.setColorAt(1, QtGui.QColor(80, 80, 100))
        gradient.setColorAt(0, QtGui.QColor(0, 0, 0))
        
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
        self.setPalette(p)
            
        # Create the banner
        self._bannerLabel = QtGui.QLabel(self)
        self._bannerLabel.setGeometry(QtCore.QRect(0, 0, width, self._bannerHeight))
        self._bannerLabel.setAutoFillBackground(True)
        self._bannerLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        
        # Set the background of the banner to black
        bp = self._bannerLabel.palette()
        bp.setColor(self._bannerLabel.backgroundRole(), QtGui.QColor(0, 0, 0))
        self._bannerLabel.setPalette(bp)
        
        # Set the banner image
        self._bannerImage = QtGui.QPixmap("images/marquee2.jpg").scaledToHeight(self._bannerHeight, mode=QtCore.Qt.SmoothTransformation)
        self._bannerLabel.setPixmap(self._bannerImage)
        self._bannerLabel.show()
        
        self.InitializeRows()
        
    def InitializeRows(self):
        self._selectedRow   = 0
        width = self.size().width()
        self._totalNumRows = self._romSource.getNumRows();         
              
        self._headers = self._romSource.getHeaders(0, -1)        
        numRows = min(self._totalNumRowsToDisplay + 2, self._totalNumRows)
                
        for row in self._rows:
            row.hide()
            
        self._rows = list()
        for i in range(0, numRows):
            count = self._romSource.getNumRoms(self._headers[(i-1) % self._totalNumRows])
            row = TileRowWidget(self, 0, self._numColsToDisplay, count, self._romSource, self._headers[(i-1) % self._totalNumRows])
            row.setGeometry(QtCore.QRect(0, self._bannerHeight + self._rowSpacing * (i-1) + self._rowHeight * (i-1), width, self._rowHeight))
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
            
        elif (key == QtCore.Qt.Key_Plus):
            self._romSourceIndex += 1
            self._romSourceIndex %= len(self._romSources)
            self._romSource = self._romSources[self._romSourceIndex]
            self.InitializeRows()
            
        elif (key == QtCore.Qt.Key_Minus):
            self._romSourceIndex -= 1
            self._romSourceIndex %= len(self._romSources)
            self._romSource = self._romSources[self._romSourceIndex]
            self.InitializeRows()
            
        print("Selected ROM: %s" % self._rows[1].GetSelectedRom().RomName())    
            
            
    ########################################################
    # Slides moves the tiles
    # @param moveDown - Set True to slide the rows down
    ########################################################
    def slideRow(self, moveDown):  
        if self._animationDone != True:
            return
          
        self._moveDown = moveDown 
        
        if moveDown:
            self._rows[0].show()
            self._rows[-1].hide()
            self._newGeometry = self._rows[0].geometry()  
        else:
            self._rows[-1].show()
            self._rows[0].hide()
            self._newGeometry = self._rows[-1].geometry()
                                        
        group = QtCore.QParallelAnimationGroup()
                
        for row in self._rows:
            animation = QtCore.QPropertyAnimation(row, "geometry")
            animation.setDuration(500)
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

    #########################################################
    # Signal for when the animation is finished and 
    # another animation can start
    #########################################################
    def animationFinished(self):
        self._rows[1].showFrame(False)        
        if self._moveDown:
            self._rows.pop(-1)
            count = self._romSource.getNumRoms(self._headers[(self._selectedRow-1)  % self._totalNumRows])                
            row = TileRowWidget(self, 0, self._numColsToDisplay, count, self._romSource, self._headers[(self._selectedRow-1) % self._totalNumRows])
            row.setGeometry(self._newGeometry)
            row.setParent(self)
            row.initialize()                        
            self._rows.insert(0, row)            
        else:            
            self._rows.pop(0)            
            count = self._romSource.getNumRoms(self._headers[(self._selectedRow+3) % self._totalNumRows])
            row = TileRowWidget(self, 0, self._numColsToDisplay, count, self._romSource, self._headers[(self._selectedRow+3) % self._totalNumRows])
            row.setGeometry(self._newGeometry)            
            row.setParent(self)            
            row.initialize()           
             
            self._rows.append(row)
           

        row.lower()
        self.repaint()
            
        self._rows[1].showFrame(True)
        self._animationDone = True
        

                
