import random, logging


class GameModel:
    
    def __init__(self):
        self.score = 0
        self.difficulty = ""
    
    def addScore(self, numberOfPoppedTiles): 
        self.score += (((numberOfPoppedTiles-4))*(numberOfPoppedTiles-3)//2)+4
        
    def setScore(self, score):
        self.score = score
    
    
    
class BoardModel:
    
    adjacentMatchingTiles = []
    
    def __init__(self):
        self.boardDimensions = (5,5)
        self.matchRequirement = 4
        self.tileModels = self.createTileModels()
        self.boardPlayable = True
        
    def getTileModels(self):
        return self.tileModels
        
    def createTileModels(self):
        tiles = []
        for y in range(self.boardDimensions[1]):
            row = []
            for x in range(self.boardDimensions[0]):
                row.append(TileModel((x,y)))
            tiles.append(row)
            
        logging.debug(f"{tiles}")
        return tiles

    def firstAvailableMove(self):
        checkedSlots = []

        for y in range(self.boardDimensions[1]):
            for x in range(self.boardDimensions[0]):
                logging.debug(f"Checking tile at coordinates ({x},{y}) for possible move...")
                if (self.tileModels[y][x] == None):
                    logging.debug(f"Coordinates ({x},{y}) has no tile.")
                    continue
                if (self.tileModels[y][x] in checkedSlots):
                    logging.debug(f"Coordinates ({x},{y}) has been checked.")
                    continue
                adjacentMatchingTiles = self.listAdjacentMatchingTiles(self.tileModels[y][x])
                if (len(adjacentMatchingTiles) < self.matchRequirement):
                    logging.debug(f"Tiles {adjacentMatchingTiles} unplayable.")
                    for tile in adjacentMatchingTiles:
                        checkedSlots.append(tile)
                    continue
                return adjacentMatchingTiles

    def isMoveAvailable(self):
        availableMove = self.firstAvailableMove()
        if availableMove:
            logging.debug(f"Payable move confirmed.")
            self.boardPlayable = True
            return True
        logging.debug("No playable moves.")
        self.boardPlayable = False
        return False

    def listEmptyTileSlots(self):
        emptySlots = []
        for y in range(self.boardDimensions[1]):
            for x in range(self.boardDimensions[0]):
                if (self.tileModels[y][x] == None):
                    corrdinates = (x,y)
                    emptySlots.append(corrdinates)
        logging.debug(f"Empty slots: {emptySlots}")
        return emptySlots
    
    def listAdjacentMatchingTiles(self, tile):  
        adjacentMatchingTiles = []      
        self.checkAdjacentTile(tile.coordinates[0], tile.coordinates[1], tile.color, adjacentMatchingTiles)
        
        return adjacentMatchingTiles

    # recurrsively checks each tile
    def checkAdjacentTile(self, x, y, color, adjacentMatchingTiles):
        logging.info(f"Checking ({x}, {y}) for adjacent matching tiles...")
        
        if (x not in range(self.boardDimensions[0]) or y not in range(self.boardDimensions[1])):
            logging.info(f"({x}, {y}) is out of bounds")
            return
        elif self.tileModels[y][x] == None:
            logging.info(f"({x}, {y}) has no tile")
            return
        elif self.tileModels[y][x] in adjacentMatchingTiles:
            logging.info(f"({x}, {y}) has already been visited")
            return
        elif (self.tileModels[y][x].getColor() != color):
            logging.info(f"({x}, {y}) is not the color {color}")
            return

        logging.info(f"Adding ({x}, {y}) to list")

        adjacentMatchingTiles.append(self.tileModels[y][x])
            
        self.checkAdjacentTile(x, y-1, color, adjacentMatchingTiles) # checks north tile
        self.checkAdjacentTile(x+1, y, color, adjacentMatchingTiles) # checks east tile
        self.checkAdjacentTile(x, y+1, color, adjacentMatchingTiles) # checks south tile
        self.checkAdjacentTile(x-1, y, color, adjacentMatchingTiles) # checks west tile

        
        
class TileModel:
    
    def __init__(self, coordinates):
        self.colors = ["blue", "green", "red"]
        self.color = self.setColor()
        self.coordinates = coordinates
                
    def setColor(self):
        color = random.choice(self.colors)
        print(color)
        return color
    
    def getColor(self):
        return self.color
            
    def setCoordinates(self, coordinates):
        self.coordinates = coordinates
        
    def getCoordinates(self):
        return self.coordinates

    def __str__(self):
        return str(f"{self.color}:{self.coordinates}")
    
    __repr__ = __str__
