# import pygame, sys, and pygame modules
import pygame, sys 
from pygame.locals import *


class DisplayView:
    
    def __init__(self, displaySize):
        self.displaySize = displaySize
        self.displaySurface = pygame.Surface(self.displaySize)
        self.displaySurface.fill((30,30,30))
        
    def getSurface(self):
        return self.displaySurface
    
    def display(self):
        self.displaySurface.blit()
        
    def fill(self, r, g, b):
        self.displaySurface.fill((r,g,b))
        
        
class BoardView:
    
    def __init__(self, boardWidth, boardHeight, parentView, boardModel):
        self.boardSize = (boardWidth, boardHeight)
        self.boardSurface = pygame.Surface(self.boardSize)
        self.parentView = parentView
        self.parentSurface = parentView.getSurface()
        self.location = (40,140)
        self.boardRect = pygame.Rect(self.location,self.boardSize)
        self.boardModel = boardModel
        self.boardDimensions = boardModel.boardDimensions
        self.tileViews = self.createTileViews()

    def getSurface(self):
        return self.boardSurface
    
    def getTileViews(self):
        return self.tileViews

    def createTileViews(self):
        tiles = []
        for y in range(self.boardDimensions[1]):
            row = []
            for x in range(self.boardDimensions[0]):
                row.append(TileView(self, self.boardModel.tileModels[y][x]))
            tiles.append(row)

        return tiles

    def display(self):
        self.parentSurface.blit(self.boardSurface,self.location)

    def fill(self, r, g, b):
        self.boardSurface.fill((r,g,b))
                
        
class TileView:
    
    def __init__(self, parentView, tileModel): 
        self.parentSurface = parentView.getSurface()
        self.tileModel = tileModel
        self.tileSize = (60, 60)
        self.tileSurface = pygame.Surface(self.tileSize)
        self.coordinates = tileModel.getCoordinates()
        self.tileRect = self.createRect()
        self.color = tileModel.color
        self.RGBcolor = self.colorTile()
        
        self.highlighted = False
            
    def updateCoordinates(self):
        self.coordinates = self.tileModel.getCoordinates()
        
    def setCoordinates(self, coordinates):
        self.coordinates = coordinates
        
    def dropRect(self):
        self.tileRect = self.tileRect.move(0, 60)
        
    def createRect(self):
        rect = self.tileSurface.get_rect()
        rect.x += 40 + 10 + 60*self.coordinates[0]
        rect.y += 140 + 10 + 60*self.coordinates[1]
        return rect
        
    def display(self):
        self.tileSurface.fill(self.RGBcolor)
        self.parentSurface.blit(self.tileSurface, ((self.coordinates[0]*60)+10, (self.coordinates[1]*60)+10))
                
    def colorTile(self):
        if (self.color == "blue"):
            return (0,0,150)
        if (self.color == "green"):
            return (0,150,0)
        if (self.color == "red"):
            return (150,0,0)
        return (0,0,0)
    
    def highlightTile(self):
        if (self.color == "blue"):
            self.RGBcolor = (50,50,200)
        if (self.color == "green"):
            self.RGBcolor = (50,200,50)
        if (self.color == "red"):
            self.RGBcolor = (200,50,50)
        self.highlighted = True
            
    def dehighlightTile(self):
        self.RGBcolor = self.colorTile()
        self.highlighted = False

    def __str__(self):
        return str(f"{self.color}:{self.coordinates}")
    
    __repr__ = __str__


class NewGameButtonView:
    
    def __init__(self, parentView):
        #self.location = (162,522) # x=(400-76)/2, y=((600-320)/4*3)+320-(16/2)
        #self.location = (124,514) # x=(400-152)/2, y=((600-320)/4*3)+320-(32/2)
        self.location = (86,506) #((400-76*3)/2, ((600-320)/4*3)+320-(16*3/2))
        self.newGameButtonRect = pygame.Rect(self.location,(76*3,16*3))
        self.newGameButtonImage = pygame.transform.scale(pygame.image.load("assets/new_game_button_image.png"), (76*3,16*3))
        self.parentView = parentView
        self.parentSurface = parentView.getSurface()
        
    def display(self):
        self.parentSurface.blit(self.newGameButtonImage, self.location)
        

class ScoreView:
    
    def __init__(self, parentView, gameModel):
        self.location = (20,20)
        self.parentSurface = parentView.getSurface()
        self.gameModel = gameModel
        self.font = pygame.font.Font("assets/press-start.regular.ttf", 25)

        
    def display(self):
        text = self.font.render(f"Score: {self.gameModel.score}", True, (255,255,255))
        self.parentSurface.blit(text, self.location)
        
class GameOverView:
    
    def __init__(self, parentView, boardModel):
        self.parentSurface = parentView.getSurface()
        self.boardModel = boardModel
        self.font = pygame.font.Font("assets/press-start.regular.ttf", 40)
        self.size = pygame.font.Font.size(self.font,"Game Over")
        self.location = (200-(self.size[0]/2),300-(self.size[1]/2))
        self.gameOver = False
        
    def setGameOver(self, gameOver):
        self.gameOver = gameOver
        
    def display(self):
        if self.gameOver:
            text = self.font.render(f"Game Over", True, (200,200,200))
            self.parentSurface.blit(text, self.location)
            
    def checkGameOver(self, isMoveAvailable):
        self.gameOver = not isMoveAvailable