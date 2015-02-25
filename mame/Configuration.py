import configparser

class Configuration(object):

    def __init__(self, configFile):
        parser = configparser.ConfigParser()
        parser.read(configFile);
        
        self._romPath = parser.get("Mame", "RomPath")
        print("romPath = %s" % self._romPath)
        self._imagePath = parser.get("Mame", "ImagePath")
        print("imagePath = %s" % self._imagePath)
        self._emulatorPath = parser.get("Mame", "EmuPath")
        self._databasePath = parser.get("Mame", "DatabasePath")
        print("dbPath = %s" % self._databasePath)
        
    def RomPath(self):
        return self._romPath
    
    def ImagePath(self):
        return self._imagePath
    
    def EmulatorPath(self):
        return self._emulatorPath
        
    def DatabasePath(self):
        return self._databasePath
