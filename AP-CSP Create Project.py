import pygame, sys

gameFrameCount = pygame.time.Clock()

from pygame.locals import *
pygame.init()

pygame.display.set_caption('2022 AP-CSP Create Project: Isometric Dungeon Crawler')

windowSize = (1100,700)

windowBase = pygame.display.set_mode(windowSize,0,32)

display = pygame.Surface((550,350))

movingRight = False
movingLeft = False
movingForward = False
movingBack = False

trueScroll = [0,0]

def loadMap(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    gameMap = []
    for row in data:
        gameMap.append(list(row))
    return gameMap

global animationFrames
animationFrames = {}

def loadAnimation(path,frameCount):
    global animationFrames
    animationName = path.split('/') [-1]
    animationFrameData = []
    n = 0
    for frame in frameCount:
        animationFrameID = animationName + '_' + str(n)
        imgLoc = path + '/' + animationFrameID + '.png'
        animationImg = pygame.image.load(imgLoc).convert()
        animationImg.set_colorkey((255,255,255))
        animationFrames[animationFrameID] = animationImg.copy()
        for i in range(frame):
            animationFrameData.append(animationFrameID)
        n += 1
    return animationFrameData

def changeAction(currentAction,frame,newAction):
    if currentAction != newAction:
        currentAction = newAction
        frame = 0
    return currentAction,frame

animationDatabase = {}

animationDatabase['idle'] = loadAnimation('animations/player1/idle',[7,7,7,7])
animationDatabase['running'] = loadAnimation('animations/player1/running',[7,7,7,7])
animationDatabase['toScreen'] = loadAnimation('animations/player1/toScreen',[7,7,7,7])

currentPlayerAction = 'idle'
playerFrame = 0
playerFlip = False

gameMap = loadMap('maps/map')

grassImg = pygame.image.load('images/isoGrass1.png')
grassImg.set_colorkey((0, 0, 0))
dirtImg = pygame.image.load('images/dirt1.png')
tileSize = grassImg.get_width()

playerHB = pygame.Rect(275,175,17,36)

backgroundObjects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

while True:
    display.fill((146,244,255))

    trueScroll[0] += (playerHB.x-trueScroll[0]-300)/20
    trueScroll[1] += (playerHB.y-trueScroll[1]-106)/20
    scroll = trueScroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,150,550,200))
    for backgroundObject in backgroundObjects:
        objRect = pygame.Rect(backgroundObject[1][0]-scroll[0]*backgroundObject[0],backgroundObject[1][1]-scroll[1]*backgroundObject[0],backgroundObject[1][2],backgroundObject[1][3])
        if backgroundObject[0] == 0.5:
            pygame.draw.rect(display,(14,222,150),objRect)
        else:
            pygame.draw.rect(display,(9,91,85),objRect)
    
    y = 0
    for layer in gameMap:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(grassImg,((x * 10 - y * 10)-scroll[0], (x * 5 + y * 5)-scroll[1]))
            x += 1
        y += 1

    playerMovement = [0,0]
    if movingRight:
        playerMovement[0] += 3
        playerHB[0] += 3
    if movingLeft:
        playerMovement[0] -= 3
        playerHB[0] -= 3
    if movingForward:
        playerHB[1] -= 3
    if movingBack:
        playerHB[1] += 3

    if playerMovement[1] > 0:
        currentPlayerAction,playerFrame = changeAction(currentPlayerAction,playerFrame,'toScreen')
        playerFlip = False
    if playerMovement[0] > 0:
        currentPlayerAction,playerFrame = changeAction(currentPlayerAction,playerFrame,'running')
        playerFlip = False
    if playerMovement[0] == 0:
        currentPlayerAction,playerFrame = changeAction(currentPlayerAction,playerFrame,'idle')
    if playerMovement[0] < 0:
        currentPlayerAction,playerFrame = changeAction(currentPlayerAction,playerFrame,'running')
        playerFlip = True
    
    playerFrame += 1
    if playerFrame >= len(animationDatabase[currentPlayerAction]):
        playerFrame = 0
    playerImgID = animationDatabase[currentPlayerAction][playerFrame]
    playerImg = animationFrames[playerImgID]
    display.blit(pygame.transform.flip(playerImg,playerFlip,False),(playerHB.x-scroll[0],playerHB.y-scroll[1]))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                movingRight = True
            if event.key == K_a:
                movingLeft = True
            if event.key == K_w:
                movingForward = True
            if event.key == K_s:
                movingBack = True
        if event.type == KEYUP:
            if event.key == K_d:
                movingRight = False
            if event.key == K_a:
                movingLeft = False
            if event.key == K_w:
                movingForward = False
            if event.key == K_s:
                movingBack = False
        
    windowBase.blit(pygame.transform.scale(display,windowSize),(0,0))
    pygame.display.update()
    gameFrameCount.tick(60)