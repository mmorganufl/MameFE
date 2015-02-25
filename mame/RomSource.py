import sqlite3
from Rom import ROM
import os

class RomSource(object):
    _config = None
    _db = None
    
    @staticmethod
    def init(config):    
        RomSource._config = config
        print("connecting to %s" % config.DatabasePath())
        RomSource._db = sqlite3.connect(config.DatabasePath())
        
    def __init__(self, type):
        self._type = type
        
    def getFavorites(self, start, count):
        cursor = RomSource._db.execute("SELECT filename, name, description, year, developer FROM games ORDER DESC BY timesPlayed LIMIT ? OFFSET ?;", (count, start))
        roms = list()        
        result = cursor.fetchall()
        for row in result:
            roms.append(ROM(row))
        return roms
    
    def validateDatabase(self):
        return
        cursor = RomSource._db.execute("SELECT filename from games;")
        result = cursor.fetchall()
        for row in result:			
            fileName = row[0]
            print("validating %s" % fileName)
            path = RomSource._config.RomPath() + os.sep + fileName + ".zip"
            exists = os.path.isfile(path)
            RomSource._db.execute("UPDATE games SET hasRom=? WHERE fileName=?;", (exists, fileName))
        
    def getNumRows(self):
        query = "SELECT COUNT(DISTINCT %s) FROM (SELECT %s FROM games WHERE hasRom=1);" % (self._type, self._type)
        print("Query = %s" % query)
        cursor = RomSource._db.execute(query)
        result = cursor.fetchall()
        return result[0][0];
        
    def getHeaders(self, start, count):
        query = "SELECT DISTINCT %s FROM (SELECT %s FROM games WHERE hasRom=1) ORDER BY %s LIMIT ? OFFSET ?;" % (self._type, self._type, self._type)
        cursor = RomSource._db.execute(query, (count, start))
        result = cursor.fetchall()
        headers = list()
        for row in result:            
            headers.append(row[0])
        return headers
    
    def getRoms(self, filter, start, count):
        query = "SELECT filename, name, description, year, developer FROM games WHERE %s=? and hasRom=1 ORDER BY name LIMIT ? OFFSET ?;" % self._type
        cursor = RomSource._db.execute(query, (filter, count, start))
        print ("start = %d, count = %d" % (start, count))
        roms = list()        
        result = cursor.fetchall()
        for row in result:
            romName = row[0]            
            imagePath = RomSource._config.ImagePath() + os.sep + romName + ".png"
            
            roms.append(ROM(row + (imagePath,)))
        
        numRoms = len(roms)
        while (numRoms < count):
            print ("getting more: start = %d, count = %d"%(0, count-numRoms))
            query = "SELECT filename, name, description, year, developer FROM games WHERE %s=? and hasRom=1 ORDER BY name LIMIT ? OFFSET ?;" % self._type        
            cursor = RomSource._db.execute(query, (filter, count-numRoms, 0))
            result = cursor.fetchall()
            for row in result:
                imagePath = RomSource._config.ImagePath() + os.sep + row[0] + ".png"            
                roms.append(ROM(row + (imagePath,)))
            numRoms = len(roms)
        return roms
    
    def getNumRoms(self, filter):
        query = "SELECT COUNT(*) FROM games WHERE %s=? and hasRom=1;" % self._type
        cursor = RomSource._db.execute(query, (filter,))
        result = cursor.fetchall()
        return result[0][0]
    

    
        
