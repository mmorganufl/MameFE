import glob

class ROM(object):

# params = (filename, name, description, year, imagePath)
    def __init__(self, params):
        self._romName = params[0]
        self._gameName = params[1]
        self._description = params[2]
        self._year = params[3]
        self._imagePath = params[4]
        
    def RomName(self):
        return self._romName
    
    def GameName(self):
        return self._gameName
    
    def Description(self):
        return self._description
    
    def Year(self):
        return self._year
    
    def ImagePath(self):
        return self._imagePath
        
        