import pygame,sys
from pygame.locals import *
pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('Create Project Dungeon Crawler')
windowSize = (1100, 700)
base = pygame.display.set_mode(windowSize, 0, 32)
screen = pygame.Surface((550, 350))

mainCharIMG = pygame.image.load('images/mainChar2.png')
mainCharIMG.set_colorkey((255, 255, 255))
grassIMG = pygame.image.load('images/grass1.png')
dirtIMG = pygame.image.load('images/dirt1.png')
tileSize = 25

def loadMap(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    gameMap = []
    for row in data:
        gameMap.append(list(row))
    return gameMap

gameMap = loadMap('map')

def collisionTest(rect, tiles):
    hitList = []
    for tile in tiles:
        if rect.colliderect(tile):
            hitList.append(tile)
    return hitList

def move(rect, movement, tiles):
    collisionTypes = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hitList = collisionTest(rect, tiles)
    for tile in hitList:
        if movement[0] > 0:
            rect.right = tile.left
            collisionTypes['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collisionTypes['left'] = True
    rect.y += movement[1]
    hitList = collisionTest(rect, tiles)
    for tile in hitList:
        if movement[1] > 0:
            rect.bottom = tile.top
            collisionTypes['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collisionTypes['top'] = True
    return rect, collisionTypes

movingRight = False
movingLeft = False
airTime = 0
scrollVal = [0, 0]
playerYMom = 0
playerHB = Rect(0, 0, mainCharIMG.get_width(), mainCharIMG.get_height())

while True:
    screen.fill((52, 174, 235))
    
    scrollVal[0] += (playerHB.x - scrollVal[0] - 263)/20
    scrollVal[1] += (playerHB.y - scrollVal[1] - 163)/20

    tileRects = []
    y = 0
    for layer in gameMap:
        x = 0
        for tile in layer:
            if tile == '1':
                screen.blit(grassIMG, (x * tileSize - scrollVal[0], y * tileSize - scrollVal[1]))
            if tile == '2':
                screen.blit(dirtIMG, (x * tileSize - scrollVal[0], y * tileSize - scrollVal[1]))
            if tile != '0':
                tileRects.append(Rect(x * tileSize, y * tileSize, tileSize, tileSize))
            x += 1
        y += 1

    playerMovement = [0, 0]
    if movingRight:
        playerMovement[0] += 2
    if movingLeft:
        playerMovement[0] -= 2
    playerMovement[1] += playerYMom
    playerYMom += 0.2
    if playerYMom > 3:
        playerYMom = 3

    playerHB, collisions = move(playerHB, playerMovement, tileRects)

    if collisions['bottom']:
        playerYMom = 0
        airTime = 0
    else:
        airTime += 1
    
    screen.blit(mainCharIMG, (playerHB.x - scrollVal[0], playerHB.y - scrollVal[1]))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                movingRight = True
            if event.key == K_a:
                movingLeft = True
            if event.key == K_SPACE:
                if airTime < 20:
                    playerYMom = -4
        if event.type == KEYUP:
            if event.key == K_d:
                movingRight = False
            if event.key == K_a:
                movingLeft = False

    base.blit(pygame.transform.scale(screen, windowSize), (0, 0))
    pygame.display.update()
    clock.tick(60)