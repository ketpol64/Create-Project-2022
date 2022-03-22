import pygame, sys
from pygame.locals import *
pygame.init()

windowSize = (400, 400)

screen = pygame.display.set_mode(windowSize, 0, 32)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.ext()

    pygame.display.update()

