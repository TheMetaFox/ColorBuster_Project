# import pygame, sys, and pygame modules
import pygame, sys 
from pygame.locals import *

# import model, view, and controller classes
from models import *
from views import *
from controller import *

# initiates pygame
pygame.init() 



# establish the calculated window
WINDOW_SIZE = (400,600) 

# initiate controller
controller = Controller()


# set the window name
pygame.display.set_caption('Color Buster') 

# initiate screen
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) 

# setup the clock
clock = pygame.time.Clock() 


# game loop
while True: 

    controller.checkEvents()
    controller.checkTimers()
    
    controller.displayViews()

    surface = controller.getDisplaySurface()
    screen.blit(surface,(0,0))
    pygame.display.update() # update display
    clock.tick(30)