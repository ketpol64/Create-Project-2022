import pygame,sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

pygame.display.set_caption('Create Project Dungeon Crawler')

windowSize = (1100, 700)

screen = pygame.display.set_mode(windowSize, 0, 32)

swordIMG = pygame.image.load('images/sword2.png')
evilFaceIMG = pygame.image.load('images/evilFace1.png')
mainCharIMG = pygame.image.load('images/heroFace1.png')

movingRight = False
movingLeft = False
playerLoc = [50, 50]
playerYMom = 0
playerHB = Rect(playerLoc[0], playerLoc[1], mainCharIMG.get_width(), mainCharIMG.get_height())

while True:

    screen.fill((52, 174, 235))

    screen.blit(mainCharIMG, playerLoc)

    if movingRight:
        playerLoc[0] += 10
    if movingLeft:
        playerLoc[0] -= 10

    if playerLoc[1] > windowSize[1]-mainCharIMG.get_height():
        playerYMom = -playerYMom
    else:
        playerYMom += 0.2
    playerLoc[1] += playerYMom

    playerHB.x = playerLoc[0]
    playerHB.y = playerLoc[1]

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