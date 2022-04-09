from tkinter import font
import pygame, sys
from pygame.locals import *
from random import randint
pygame.init()
pygame.display.set_caption('2022 AP-CSP Create Project: Isometric Dungeon Crawler')

gameFrameCount = pygame.time.Clock()

windowSize = (1100,700)
windowBase = pygame.display.set_mode(windowSize,0,32)

font100 = pygame.font.SysFont(None,100)
font75 = pygame.font.SysFont(None,80)

def drawText(text,font,color,surface,x,y):
    textObj = font.render(text,1,color)
    textRect = textObj.get_rect()
    textRect.topleft = (x,y)
    surface.blit(textObj,textRect)

def loadMap(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    gameMap = []
    for row in data:
        gameMap.append(list(row))
    return gameMap

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

def collisionTest(rect,tiles):
    hitList = []
    for tile in tiles:
        if rect.colliderect(tile):
            hitList.append(tile)
    return hitList

def move(rect,movement,tiles):
    collisionTypes = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hitList = collisionTest(rect,tiles)
    for tile in hitList:
        if movement[0] > 0:
            rect.right = tile.left
            collisionTypes['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collisionTypes['left'] = True
    rect.y += movement[1]
    hitList = collisionTest(rect,tiles)
    for tile in hitList:
        if movement[1] > 0:
            rect.bottom = tile.top
            collisionTypes['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collisionTypes['top'] = True
    return rect, collisionTypes

def lOne(levelOne):
    display = pygame.Surface((550,350))

    movingRight = False
    movingLeft = False
    verticalMom = 0
    airTime = 0
    trueScroll = [0,0]

    global animationFrames
    animationFrames = {}
    animationDatabase = {}
    animationDatabase['idle'] = loadAnimation('animations/player1/idle',[7,7,7,7])
    animationDatabase['running'] = loadAnimation('animations/player1/running',[7,7,7,7]) 
    currentPlayerAction = 'idle'
    playerFrame = 0
    playerFlip = False

    gameMap = loadMap('maps/map1')
    grassImg = pygame.image.load('images/grass1.png')
    dirtImg = pygame.image.load('images/dirt1.png')
    tileSize = grassImg.get_width()
    backgroundObjects = [[0.25,[150,randint(20,150),randint(50,150),700]],
                        [0.25,[300,randint(20,150),randint(50,150),700]],
                        [0.25,[450,randint(20,150),randint(50,150),700]],
                        [0.25,[600,randint(20,150),randint(50,150),700]],
                        [0.25,[750,randint(20,150),randint(50,150),700]],
                        [0.25,[900,randint(20,150),randint(50,150),700]],
                        [0.25,[1050,randint(20,150),randint(50,150),700]],
                        [0.25,[1250,randint(20,150),randint(50,150),700]],
                        [0.25,[1350,randint(20,150),randint(50,150),700]],
                        [0.5,[250,randint(80,250),randint(40,100),550]],
                        [0.5,[450,randint(80,250),randint(40,100),550]],
                        [0.5,[650,randint(80,250),randint(40,100),550]],
                        [0.5,[850,randint(80,250),randint(40,100),550]],
                        [0.5,[1050,randint(80,250),randint(40,100),550]],
                        [0.5,[1250,randint(80,250),randint(40,100),550]],
                        [0.75,[200,randint(250,450),randint(20,80),700]],
                        [0.75,[300,randint(250,450),randint(20,80),700]],
                        [0.75,[400,randint(250,450),randint(20,80),700]],
                        [0.75,[500,randint(250,450),randint(20,80),700]],
                        [0.75,[600,randint(250,450),randint(20,80),700]],
                        [0.75,[700,randint(250,450),randint(20,80),700]],
                        [0.75,[800,randint(250,450),randint(20,80),700]],
                        [0.75,[900,randint(250,450),randint(20,80),700]],
                        [0.75,[1000,randint(250,450),randint(20,80),700]],
                        [0.75,[1100,randint(250,450),randint(20,80),700]],
                        [0.75,[1200,randint(250,450),randint(20,80),700]],
                        [0.75,[1300,randint(250,450),randint(20,80),700]],
                        [0.75,[1400,randint(250,450),randint(20,80),700]],
                        [0.75,[1500,randint(250,450),randint(20,80),700]],
                        [0.75,[1600,randint(250,450),randint(20,80),700]],
                        [0.75,[1700,randint(250,450),randint(20,80),700]],
                        [0.75,[1800,randint(250,450),randint(20,80),700]],
                        [0.75,[1900,randint(250,450),randint(20,80),700]],
                        [0.75,[2000,randint(250,450),randint(20,80),700]],
                        [0.75,[2100,randint(250,450),randint(20,80),700]],]

    playerHB = pygame.Rect(300,160,17,36)

    while levelOne:
        display.fill((146,244,255))

        trueScroll[0] += (playerHB.x-trueScroll[0]-260)/20
        trueScroll[1] += (playerHB.y-trueScroll[1]-157)/20
        scroll = trueScroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        pygame.draw.rect(display,(7,80,75),pygame.Rect(0,150,550,200))
        for backgroundObject in backgroundObjects:
            objRect = pygame.Rect(backgroundObject[1][0]-scroll[0]*backgroundObject[0],backgroundObject[1][1]-scroll[1]*backgroundObject[0],backgroundObject[1][2],backgroundObject[1][3])
            if backgroundObject[0] == 0.5:
                pygame.draw.rect(display,(14,222,150),objRect)
            elif backgroundObject[0] == 0.25:
                pygame.draw.rect(display,(9,91,85),objRect)
            elif backgroundObject[0] == 0.75:
                pygame.draw.rect(display,(24,217,162),objRect)

        tileRects = []
        y = 0
        for layer in gameMap:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(grassImg,(x*tileSize-scroll[0],y*tileSize-scroll[1]))
                if tile == '2':
                    display.blit(dirtImg,(x*tileSize-scroll[0],y*tileSize-scroll[1]))
                if tile != '0':
                    tileRects.append(pygame.Rect(x*tileSize,y*tileSize,tileSize,tileSize))
                x += 1
            y += 1

        playerMovement = [0,0]
        if movingRight:
            playerMovement[0] += 3
        if movingLeft:
            playerMovement[0] -= 3
        playerMovement[1] += verticalMom
        verticalMom += 0.2
        if verticalMom > 3:
            verticalMom = 3

        if playerMovement[0] > 0:
            currentPlayerAction,playerFrame = changeAction(currentPlayerAction,playerFrame,'running')
            playerFlip = False
        if playerMovement[0] == 0:
            currentPlayerAction,playerFrame = changeAction(currentPlayerAction,playerFrame,'idle')
        if playerMovement[0] < 0:
            currentPlayerAction,playerFrame = changeAction(currentPlayerAction,playerFrame,'running')
            playerFlip = True

        playerHB,collisions = move(playerHB,playerMovement,tileRects)
        if collisions['bottom']:
            airTime = 0
            verticalMom = 0
        else:
            airTime += 1
        if collisions['top']:
            verticalMom = 0

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
                if event.key == K_ESCAPE:
                    inGameMenu(True)
                if event.key == K_d:
                    movingRight = True
                if event.key == K_a:
                    movingLeft = True
                if event.key == K_SPACE:
                    if airTime < 20:
                        verticalMom = -5
            if event.type == KEYUP:
                if event.key == K_d:
                    movingRight = False
                if event.key == K_a:
                    movingLeft = False

        windowBase.blit(pygame.transform.scale(display,windowSize),(0,0))
        pygame.display.update()
        gameFrameCount.tick(60)

def lTwo(levelTwo):
    display = pygame.Surface((550,350))

    movingRight = False
    movingLeft = False
    verticalMom = 0
    airTime = 0
    trueScroll = [0,0]

    global animationFrames
    animationFrames = {}
    animationDatabase = {}
    animationDatabase['idle'] = loadAnimation('animations/player1/idle',[7,7,7,7])
    animationDatabase['running'] = loadAnimation('animations/player1/running',[7,7,7,7]) 
    currentPlayerAction = 'idle'
    playerFrame = 0
    playerFlip = False

    gameMap = loadMap('maps/map2')
    grassImg = pygame.image.load('images/grass1.png')
    dirtImg = pygame.image.load('images/dirt1.png')
    tileSize = grassImg.get_width()
    backgroundObjects = [[0.25,[150,randint(20,150),randint(50,150),700]],
                        [0.25,[300,randint(20,150),randint(50,150),700]],
                        [0.25,[450,randint(20,150),randint(50,150),700]],
                        [0.25,[600,randint(20,150),randint(50,150),700]],
                        [0.25,[750,randint(20,150),randint(50,150),700]],
                        [0.25,[900,randint(20,150),randint(50,150),700]],
                        [0.25,[1050,randint(20,150),randint(50,150),700]],
                        [0.25,[1250,randint(20,150),randint(50,150),700]],
                        [0.25,[1350,randint(20,150),randint(50,150),700]],
                        [0.5,[250,randint(80,250),randint(40,100),550]],
                        [0.5,[450,randint(80,250),randint(40,100),550]],
                        [0.5,[650,randint(80,250),randint(40,100),550]],
                        [0.5,[850,randint(80,250),randint(40,100),550]],
                        [0.5,[1050,randint(80,250),randint(40,100),550]],
                        [0.5,[1250,randint(80,250),randint(40,100),550]],
                        [0.75,[200,randint(250,450),randint(20,80),700]],
                        [0.75,[300,randint(250,450),randint(20,80),700]],
                        [0.75,[400,randint(250,450),randint(20,80),700]],
                        [0.75,[500,randint(250,450),randint(20,80),700]],
                        [0.75,[600,randint(250,450),randint(20,80),700]],
                        [0.75,[700,randint(250,450),randint(20,80),700]],
                        [0.75,[800,randint(250,450),randint(20,80),700]],
                        [0.75,[900,randint(250,450),randint(20,80),700]],
                        [0.75,[1000,randint(250,450),randint(20,80),700]],
                        [0.75,[1100,randint(250,450),randint(20,80),700]],
                        [0.75,[1200,randint(250,450),randint(20,80),700]],
                        [0.75,[1300,randint(250,450),randint(20,80),700]],
                        [0.75,[1400,randint(250,450),randint(20,80),700]],
                        [0.75,[1500,randint(250,450),randint(20,80),700]],
                        [0.75,[1600,randint(250,450),randint(20,80),700]],
                        [0.75,[1700,randint(250,450),randint(20,80),700]],
                        [0.75,[1800,randint(250,450),randint(20,80),700]],
                        [0.75,[1900,randint(250,450),randint(20,80),700]],
                        [0.75,[2000,randint(250,450),randint(20,80),700]],
                        [0.75,[2100,randint(250,450),randint(20,80),700]],]

    playerHB = pygame.Rect(300,160,17,36)

    while levelTwo:
        display.fill((146,244,255))

        trueScroll[0] += (playerHB.x-trueScroll[0]-260)/20
        trueScroll[1] += (playerHB.y-trueScroll[1]-157)/20
        scroll = trueScroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        pygame.draw.rect(display,(7,80,75),pygame.Rect(0,150,550,200))
        for backgroundObject in backgroundObjects:
            objRect = pygame.Rect(backgroundObject[1][0]-scroll[0]*backgroundObject[0],backgroundObject[1][1]-scroll[1]*backgroundObject[0],backgroundObject[1][2],backgroundObject[1][3])
            if backgroundObject[0] == 0.5:
                pygame.draw.rect(display,(14,222,150),objRect)
            elif backgroundObject[0] == 0.25:
                pygame.draw.rect(display,(9,91,85),objRect)
            elif backgroundObject[0] == 0.75:
                pygame.draw.rect(display,(24,217,162),objRect)

        tileRects = []
        y = 0
        for layer in gameMap:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(grassImg,(x*tileSize-scroll[0],y*tileSize-scroll[1]))
                if tile == '2':
                    display.blit(dirtImg,(x*tileSize-scroll[0],y*tileSize-scroll[1]))
                if tile != '0':
                    tileRects.append(pygame.Rect(x*tileSize,y*tileSize,tileSize,tileSize))
                x += 1
            y += 1

        playerMovement = [0,0]
        if movingRight:
            playerMovement[0] += 3
        if movingLeft:
            playerMovement[0] -= 3
        playerMovement[1] += verticalMom
        verticalMom += 0.2
        if verticalMom > 3:
            verticalMom = 3

        if playerMovement[0] > 0:
            currentPlayerAction,playerFrame = changeAction(currentPlayerAction,playerFrame,'running')
            playerFlip = False
        if playerMovement[0] == 0:
            currentPlayerAction,playerFrame = changeAction(currentPlayerAction,playerFrame,'idle')
        if playerMovement[0] < 0:
            currentPlayerAction,playerFrame = changeAction(currentPlayerAction,playerFrame,'running')
            playerFlip = True

        playerHB,collisions = move(playerHB,playerMovement,tileRects)
        if collisions['bottom']:
            airTime = 0
            verticalMom = 0
        else:
            airTime += 1
        if collisions['top']:
            verticalMom = 0

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
                if event.key == K_ESCAPE:
                    inGameMenu(True)
                if event.key == K_d:
                    movingRight = True
                if event.key == K_a:
                    movingLeft = True
                if event.key == K_SPACE:
                    if airTime < 20:
                        verticalMom = -5
            if event.type == KEYUP:
                if event.key == K_d:
                    movingRight = False
                if event.key == K_a:
                    movingLeft = False

        windowBase.blit(pygame.transform.scale(display,windowSize),(0,0))
        pygame.display.update()
        gameFrameCount.tick(60)

def lThree(levelThree):
    display = pygame.Surface((550,350))

    movingRight = False
    movingLeft = False
    verticalMom = 0
    airTime = 0
    trueScroll = [0,0]

    global animationFrames
    animationFrames = {}
    animationDatabase = {}
    animationDatabase['idle'] = loadAnimation('animations/player1/idle',[7,7,7,7])
    animationDatabase['running'] = loadAnimation('animations/player1/running',[7,7,7,7]) 
    currentPlayerAction = 'idle'
    playerFrame = 0
    playerFlip = False

    gameMap = loadMap('maps/map3')
    grassImg = pygame.image.load('images/grass1.png')
    dirtImg = pygame.image.load('images/dirt1.png')
    tileSize = grassImg.get_width()
    backgroundObjects = [[0.25,[150,randint(20,150),randint(50,150),700]],
                        [0.25,[300,randint(20,150),randint(50,150),700]],
                        [0.25,[450,randint(20,150),randint(50,150),700]],
                        [0.25,[600,randint(20,150),randint(50,150),700]],
                        [0.25,[750,randint(20,150),randint(50,150),700]],
                        [0.25,[900,randint(20,150),randint(50,150),700]],
                        [0.25,[1050,randint(20,150),randint(50,150),700]],
                        [0.25,[1250,randint(20,150),randint(50,150),700]],
                        [0.25,[1350,randint(20,150),randint(50,150),700]],
                        [0.5,[250,randint(80,250),randint(40,100),550]],
                        [0.5,[450,randint(80,250),randint(40,100),550]],
                        [0.5,[650,randint(80,250),randint(40,100),550]],
                        [0.5,[850,randint(80,250),randint(40,100),550]],
                        [0.5,[1050,randint(80,250),randint(40,100),550]],
                        [0.5,[1250,randint(80,250),randint(40,100),550]],
                        [0.75,[200,randint(250,450),randint(20,80),700]],
                        [0.75,[300,randint(250,450),randint(20,80),700]],
                        [0.75,[400,randint(250,450),randint(20,80),700]],
                        [0.75,[500,randint(250,450),randint(20,80),700]],
                        [0.75,[600,randint(250,450),randint(20,80),700]],
                        [0.75,[700,randint(250,450),randint(20,80),700]],
                        [0.75,[800,randint(250,450),randint(20,80),700]],
                        [0.75,[900,randint(250,450),randint(20,80),700]],
                        [0.75,[1000,randint(250,450),randint(20,80),700]],
                        [0.75,[1100,randint(250,450),randint(20,80),700]],
                        [0.75,[1200,randint(250,450),randint(20,80),700]],
                        [0.75,[1300,randint(250,450),randint(20,80),700]],
                        [0.75,[1400,randint(250,450),randint(20,80),700]],
                        [0.75,[1500,randint(250,450),randint(20,80),700]],
                        [0.75,[1600,randint(250,450),randint(20,80),700]],
                        [0.75,[1700,randint(250,450),randint(20,80),700]],
                        [0.75,[1800,randint(250,450),randint(20,80),700]],
                        [0.75,[1900,randint(250,450),randint(20,80),700]],
                        [0.75,[2000,randint(250,450),randint(20,80),700]],
                        [0.75,[2100,randint(250,450),randint(20,80),700]],]

    playerHB = pygame.Rect(300,160,17,36)

    while levelThree:
        display.fill((146,244,255))

        trueScroll[0] += (playerHB.x-trueScroll[0]-260)/20
        trueScroll[1] += (playerHB.y-trueScroll[1]-157)/20
        scroll = trueScroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        pygame.draw.rect(display,(7,80,75),pygame.Rect(0,150,550,200))
        for backgroundObject in backgroundObjects:
            objRect = pygame.Rect(backgroundObject[1][0]-scroll[0]*backgroundObject[0],backgroundObject[1][1]-scroll[1]*backgroundObject[0],backgroundObject[1][2],backgroundObject[1][3])
            if backgroundObject[0] == 0.5:
                pygame.draw.rect(display,(14,222,150),objRect)
            elif backgroundObject[0] == 0.25:
                pygame.draw.rect(display,(9,91,85),objRect)
            elif backgroundObject[0] == 0.75:
                pygame.draw.rect(display,(24,217,162),objRect)

        tileRects = []
        y = 0
        for layer in gameMap:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(grassImg,(x*tileSize-scroll[0],y*tileSize-scroll[1]))
                if tile == '2':
                    display.blit(dirtImg,(x*tileSize-scroll[0],y*tileSize-scroll[1]))
                if tile != '0':
                    tileRects.append(pygame.Rect(x*tileSize,y*tileSize,tileSize,tileSize))
                x += 1
            y += 1

        playerMovement = [0,0]
        if movingRight:
            playerMovement[0] += 3
        if movingLeft:
            playerMovement[0] -= 3
        playerMovement[1] += verticalMom
        verticalMom += 0.2
        if verticalMom > 3:
            verticalMom = 3

        if playerMovement[0] > 0:
            currentPlayerAction,playerFrame = changeAction(currentPlayerAction,playerFrame,'running')
            playerFlip = False
        if playerMovement[0] == 0:
            currentPlayerAction,playerFrame = changeAction(currentPlayerAction,playerFrame,'idle')
        if playerMovement[0] < 0:
            currentPlayerAction,playerFrame = changeAction(currentPlayerAction,playerFrame,'running')
            playerFlip = True

        playerHB,collisions = move(playerHB,playerMovement,tileRects)
        if collisions['bottom']:
            airTime = 0
            verticalMom = 0
        else:
            airTime += 1
        if collisions['top']:
            verticalMom = 0

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
                if event.key == K_ESCAPE:
                    inGameMenu(True)
                if event.key == K_d:
                    movingRight = True
                if event.key == K_a:
                    movingLeft = True
                if event.key == K_SPACE:
                    if airTime < 20:
                        verticalMom = -5
            if event.type == KEYUP:
                if event.key == K_d:
                    movingRight = False
                if event.key == K_a:
                    movingLeft = False

        windowBase.blit(pygame.transform.scale(display,windowSize),(0,0))
        pygame.display.update()
        gameFrameCount.tick(60)

def mainMenu():
    click = False
    while True:
        windowBase.fill((146,244,255))
        drawText('Main Menu',font100,(255,255,255),windowBase,20,20)

        mx,my = pygame.mouse.get_pos()

        b1 = pygame.Rect(150,175,800,100)
        b2 = pygame.Rect(150,325,800,100)
        b3 = pygame.Rect(150,475,800,100)
        if b1.collidepoint((mx,my)):
            if click:
                lOne(True)
        if b2.collidepoint((mx,my)):
            if click:
                lTwo(True)
        if b3.collidepoint((mx,my)):
            if click:
                lThree(True)
        pygame.draw.rect(windowBase,(255,255,255),b1)
        drawText('Level One',font75,(146,244,255),windowBase,400,200)
        pygame.draw.rect(windowBase,(255,255,255),b2)
        drawText('Level Two',font75,(146,244,255),windowBase,405,350)
        pygame.draw.rect(windowBase,(255,255,255),b3)
        drawText('Level Three',font75,(146,244,255),windowBase,385,500)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        gameFrameCount.tick(60)

def inGameMenu(igMenu):
    igClick = False
    while igMenu:
        windowBase.fill((146,244,255))
        drawText('Main Menu',font100,(255,255,255),windowBase,20,20)

        mx,my = pygame.mouse.get_pos()

        b1 = pygame.Rect(150,175,800,100)
        b2 = pygame.Rect(150,325,800,100)
        if b1.collidepoint((mx,my)):
            if igClick:
                igMenu = False
        if b2.collidepoint((mx,my)):
            if igClick:
                mainMenu()
        pygame.draw.rect(windowBase,(255,255,255),b1)
        drawText('Back',font75,(146,244,255),windowBase,485,200)
        pygame.draw.rect(windowBase,(255,255,255),b2)
        drawText('Menu',font75,(146,244,255),windowBase,475,350)

        igClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    levelThree = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    igClick = True

        pygame.display.update()
        gameFrameCount.tick(60)

mainMenu()