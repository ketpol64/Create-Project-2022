import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

pygame.display.set_caption('Create Project Dungeon Crawler')

windowSize = (1100, 700)

screen = pygame.display.set_mode(windowSize, 0, 32)

swordIMG = pygame.image.load('sword2.png')
evilFaceIMG = pygame.image.load('evilFace1.png')

movingRight = False
movingLeft = False

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                movingRight = True
            if event.key == K_a:
                movingLeft = True
        if event.type == KEYUP:
            if event.key == K_d:
                movingRight = False
            if event.key == K_a:
                movingLeft = False

    pygame.display.update()
    clock.tick(60)