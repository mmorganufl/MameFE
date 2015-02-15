import configparser

class Configuration(object):

    def __init__(self, configFile):
        parser = configparser.ConfigParser()
        parser.read("mamefe.ini");
        
        self._romPath = parser.get("Mame", "RomPath")
        self._imagePath = parser.get("Mame", "ImagePath")
        self._emulatorPath = parser.get("Mame", "EmuPath")
        self._databasePath = parser.get("Mame", "DatabasePath")
        
    def RomPath(self):
        return self._romPath
    
    def ImagePath(self):
        return self._imagePath
    
    def EmulatorPath(self):
        return self._emulatorPath
        
    def DatabasePath(self):
        return self._databasePath