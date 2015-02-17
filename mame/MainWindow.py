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
        
              
        self._headers = self._romSource.getHeaders(0, 50)        
        numRows = min(3, len(self._headers))
                
        for i in range(0, numRows):
            count = self._romSource.getNumRoms(self._headers[i])
            row = TileRowWidget(1, 3, count, self._romSource, self._headers[i])
            row.setGeometry(QtCore.QRect(0, bannerHeight + self._rowSpacing * i + self._rowHeight * i, width, self._rowHeight))
            row.setParent(self)
            row.initialize()
            row.showFrame(i == 0)
            row.lower()
            self._rows.append(row)
        
        self._bannerLabel.raise_()
                       
   
    def keyPressEvent(self, e):
        key = e.key()  
        if (key == QtCore.Qt.Key_Left):      
            self._rows[0].slideTiles(True)
            
        elif (key == QtCore.Qt.Key_Right):
            self._rows[0].slideTiles(False) 
            
        elif (key == QtCore.Qt.Key_Down):
            if (self._selectedRow > 0):
                self._selectedRow -= 1
                self.slideRow(True)          
            
        elif (key == QtCore.Qt.Key_Up):
            if (self._selectedRow < (len(self._headers) - 1)):                            
                self._selectedRow += 1
                self.slideRow(False)                  
                
      
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
               
        
        self._rows[0].showFrame(False)        
        if self._moveDown:
            self._rows.pop(-1)
            count = self._romSource.getNumRoms(self._headers[self._selectedRow])                
            row = TileRowWidget(1, 3, count, self._romSource, self._headers[self._selectedRow])
            row.setGeometry(self._newGeometry)
            row.setParent(self)
            row.initialize()                        
            self._rows.insert(0, row)            
        else:
            self._rows.pop(0)
            count = self._romSource.getNumRoms(self._headers[self._selectedRow+1])
            row = TileRowWidget(1, 3, count, self._romSource, self._headers[self._selectedRow+1])
            row.setGeometry(self._newGeometry)            
            row.setParent(self)            
            row.initialize()           
             
            self._rows.append(row)
            
        self._rows[0].showFrame(True)
        print("there are %d row" % len(self._rows))

    #########################################################
    # Signal for when the animation is finished and 
    # another animation can start
    #########################################################
    def animationFinished(self):
        self._animationDone = True
                
