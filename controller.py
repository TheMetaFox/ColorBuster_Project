from models import *
from views import *
import logging

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] - %(message)s")

class Controller:
    
    boardDimensions = (5,5)
    adjacentMatchingTiles = []
    

    
    def __init__(self):
        self.gameModel = GameModel()
        self.boardModel = BoardModel()
        self.tileModels = self.boardModel.getTileModels()
        
        self.displayView = DisplayView((400, 600))
        self.newGameButtonView = NewGameButtonView(self.displayView)
        self.scoreView = ScoreView(self.displayView, self.gameModel)
        self.gameOverView = GameOverView(self.displayView, self.boardModel)
        self.boardView = BoardView(320, 320, self.displayView, self.boardModel)
        self.tileViews = self.boardView.getTileViews()
        
        self.m_key_down = False
        self.mute_music = False
        pygame.mixer.music.load('assets/music_1.mp3')
        pygame.mixer.music.play(-1)
        self.popSound = pygame.mixer.Sound('assets/pop_click.wav')
        self.dullSound = pygame.mixer.Sound('assets/dull_click.wav')
        
        self.hintTimer = 0
        
        logging.debug(f"\n\tTile Models: \n\t{self.tileModels[0]}\n\t{self.tileModels[1]}\n\t{self.tileModels[2]}\n\t{self.tileModels[3]}\n\t{self.tileModels[4]}\n\tTile Views: \n\t{self.tileViews[0]}\n\t{self.tileViews[1]}\n\t{self.tileViews[2]}\n\t{self.tileViews[3]}\n\t{self.tileViews[4]}")
        
        
    def getDisplayView(self):
        return self.displayView
        

    def getDisplaySurface(self):
        return self.displayView.getSurface()


    def displayViews(self):
        self.displayView.fill(30,30,30)
        self.newGameButtonView.display()
        self.scoreView.display()
        self.boardView.fill(70,70,70)
        for y in range(self.boardDimensions[1]):
            for x in range(self.boardDimensions[0]):
                if (self.tileViews[y][x] == None):
                    #logging.warning(f"Cannot display none tile at ({x},{y})")
                    continue
                self.tileViews[y][x].display()
        self.boardView.display()
        self.gameOverView.display()


    def checkEvents(self):
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                self.quit()
            if event.type == MOUSEMOTION:
                self.highlightView(pygame.mouse.get_pos())
                self.hintTimer = 0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.onClick(pygame.mouse.get_pos())
            if event.type == KEYDOWN:
                if event.key == K_m:
                    if self.m_key_down == False:
                        self.mute_music = self.mute_music == False
                    if self.mute_music == True:
                        pygame.mixer.music.fadeout(1000)
                    if self.mute_music == False:
                        pygame.mixer.music.play(-1)
                self.m_key_down = True
            if event.type == KEYUP: # check for key up
                if event.key == K_m:
                    self.m_key_down = False


    
    def checkTimers(self):

        if self.hintTimer == 150: # ~5 seconds
            self.showHint()
        
    
        if self.hintTimer <= 150 and self.boardModel.boardPlayable:
            logging.debug(f"Hint timer: {self.hintTimer}...")
            self.hintTimer += 1

        

    def showHint(self):
        logging.info(f"Showing hint...")
        for tile in self.boardModel.firstAvailableMove():
            self.tileViews[tile.getCoordinates()[1]][tile.getCoordinates()[0]].highlightTile()
            
        

    def onClick(self, mousePosition):
        if self.boardView.boardRect.collidepoint(mousePosition):
            for y in range(self.boardDimensions[1]):
                for x in range(self.boardDimensions[0]):
                    logging.debug(f"Checking tile at coordinates ({x},{y}) for click...")
                    if (self.tileViews[y][x] == None):
                        logging.error(f"Coordinates ({x},{y}) has no tile.")
                    elif (self.tileViews[y][x].tileRect.collidepoint(mousePosition)):
                        self.onTileClick(self.tileModels[y][x])
                        self.hintTimer = 0
                        return
        elif self.newGameButtonView.newGameButtonRect.collidepoint(mousePosition):
            logging.debug(f"New Game button clicked...") 
            while True:
                self.destroyAllTiles()
                self.refillBoard()
                if self.boardModel.isMoveAvailable():
                    break
            self.gameOverView.setGameOver(False)
            self.gameModel.setScore(0)
        else:
            logging.debug(f"Void click... ")


    def highlightView(self, mousePosition):    
        for y in range(self.boardDimensions[1]):
            for x in range(self.boardDimensions[0]):
                if (self.tileViews[y][x] == None):
                    logging.warning(f"Cannot highlight none tile at ({x},{y})")
                    continue
            
                if (self.tileViews[y][x].tileRect.collidepoint(mousePosition)):
                    self.tileViews[y][x].highlightTile()
                elif (self.tileViews[y][x].highlighted == True):
                    self.tileViews[y][x].dehighlightTile()



    def onTileClick(self, tile):

        matchingTileList = self.boardModel.listAdjacentMatchingTiles(tile)

        print(matchingTileList)
        if len(matchingTileList) < self.boardModel.matchRequirement:
            logging.info(f"Number of adjacent tiles is too short...")
            self.dullSound.play()
            return

        self.destroyTiles(matchingTileList)
        self.popSound.play()

        self.gameModel.addScore(len(matchingTileList))

        self.adjustTiles()

        self.refillBoard()

        self.gameOverView.checkGameOver(self.boardModel.isMoveAvailable())
        logging.debug(f"\nTile Models: \n{self.tileModels[0]}\n{self.tileModels[1]}\n{self.tileModels[2]}\n{self.tileModels[3]}\n{self.tileModels[4]}\nTile Views: \n{self.tileViews[0]}\n{self.tileViews[1]}\n{self.tileViews[2]}\n{self.tileViews[3]}\n{self.tileViews[4]}")


    def destroyTiles(self, tileList):
        logging.info(f"Destroying tiles: {tileList}")
        for tile in tileList:            
            self.tileModels[tile.coordinates[1]][tile.coordinates[0]] = None
            self.tileViews[tile.coordinates[1]][tile.coordinates[0]] = None
            
    
    def destroyAllTiles(self):
        logging.info(f"Destroying all tiles")
        for y in range(self.boardDimensions[1]):
            for x in range(self.boardDimensions[0]):
                self.tileModels[y][x] = None
                self.tileViews[y][x] = None


    
    def adjustTiles(self):
        emptySlots = self.boardModel.listEmptyTileSlots()
        for slot in emptySlots:
            i = 0
            for row in range(slot[1],0,-1):
                logging.debug(f"Moving slot ({slot[0]}, {row-1}) to ({slot[0]}, {row})")
                self.tileModels[row][slot[0]] = self.tileModels[row-1][slot[0]]
                self.tileViews[row][slot[0]] = self.tileViews[row-1][slot[0]]
                if self.tileModels[row][slot[0]] == None:
                    continue
                if row == 1:
                    self.tileModels[0][slot[0]] = None
                    self.tileViews[0][slot[0]] = None

                self.tileModels[row][slot[0]].setCoordinates((slot[0],row))
                self.tileViews[row][slot[0]].updateCoordinates()
                self.tileViews[row][slot[0]].dropRect()


                    
    
    def refillBoard(self):
        emptySlots = self.boardModel.listEmptyTileSlots()
        
        for slot in emptySlots:
            self.tileModels[slot[1]][slot[0]] = TileModel((slot[0],slot[1]))
            self.tileViews[slot[1]][slot[0]] = TileView(self.boardView, self.tileModels[slot[1]][slot[0]])
        
        

    def quit(self):
        pygame.quit() # stop pygame
        sys.exit() # stop script
