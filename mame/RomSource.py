import sqlite3
from mame.Rom import ROM
import os

class RomSource(object):
    def __init__(self, config):
        self._config = config
        self._db = sqlite3.connect(config.DatabasePath())
        
    def getFavorites(self, start, count):
        cursor = self._db.execute("SELECT filename, name, description FROM games ORDER DESC BY timesPlayed LIMIT ? OFFSET ?;", (count, start))
        roms = list()        
        result = cursor.fetchall()
        for row in result:
            roms.append(ROM(row))
        return roms

class GenreRomSource(RomSource):
    def __init__(self, config):
        RomSource.__init__(self, config);
        
    def getNumRows(self):
        cursor = self._db.execute("SELECT COUNT(DISTINCT genre) FROM games;")
        result = cursor.fetchall()
        return result[0][0];
        
    def getHeaders(self, start, count):
        cursor = self._db.execute("SELECT DISTINCT genre FROM games ORDER BY genre LIMIT ? OFFSET ?;", (count, start))
        result = cursor.fetchall()
        genres = list()
        for row in result:            
            genres.append(row[0])
        return genres
    
    def getRoms(self, genre, start, count):
        cursor = self._db.execute("SELECT filename, name, description, year FROM games WHERE genre=? ORDER BY name LIMIT ? OFFSET ?;", (genre, count, start))
        print ("start = %d, count = %d"%(start, count))
        roms = list()        
        result = cursor.fetchall()
        for row in result:            
            imagePath = self._config.ImagePath() + os.sep + row[0] + ".png"            
            roms.append(ROM(row + (imagePath,)))
        
        numRoms = len(result)
        if (numRoms < count):
            print ("getting more: start = %d, count = %d"%(0, count-numRoms))
            cursor = self._db.execute("SELECT filename, name, description, year FROM games WHERE genre=? ORDER BY name LIMIT ? OFFSET ?;", (genre, count-numRoms, 0))
            result = cursor.fetchall()
            for row in result:
                imagePath = self._config.ImagePath() + os.sep + row[0] + ".png"            
                roms.append(ROM(row + (imagePath,)))
        return roms
    
    def getNumRoms(self, genre):
        cursor = self._db.execute("SELECT COUNT(*) FROM games WHERE genre=?;", (genre,))
        result = cursor.fetchall()
        return result[0][0]
    
class YearRomSource(RomSource):
    def getNumRows(self):
        cursor = self._db.execute("SELECT COUNT(DISTINCT year) FROM games;")
        result = cursor.fetchall()
        return result[0][0];
    
    def getHeaders(self, start, count):
        cursor = self._db.execute("SELECT DISTINCT year FROM games ORDER BY genre LIMIT ? OFFSET ?;", (count, start))
        result = cursor.fetchall()
        years = list()
        for row in result:
            years.append(row[0])
        return years
    
    def getRoms(self, year, start, count):
        cursor = self._db.execute("SELECT filename, name, description, year FROM games WHERE year=? ORDER BY name LIMIT ? OFFSET ?;", (year, count, start))
        roms = list()        
        result = cursor.fetchall()
        for row in result:
            roms.append(ROM(row))
        return roms
    
    def getNumRoms(self, year):
        cursor = self._db.execute("SELECT count(*) FROM games WHERE year=?;", (year,))
        result = cursor.fetchall()
        return result[0][0]
    
        