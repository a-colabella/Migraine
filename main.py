# Migraine
# An arcade game that combines elements of
# snake, tetris, space invaders, potentially more?
import pygame
from random import randint
import copy

SIZE = 25
TICK = 5
#TICK = 100 # Cheat mode
BLOCK_SPEED = 1
SHIP_SPEED = 1
BULLET_SPEED = 2

# Initialize
pygame.init()

# Display
winfo = pygame.display.Info()
#WIDTH, HEIGHT = (winfo.current_w / 2, winfo.current_h)
WIDTH, HEIGHT = (500, 950)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# Caption
pygame.display.set_caption('Migraine')
pygame.display.update()

#
class posn:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def against(self, p, o):
        xDiff = self.x - p.x
        yDiff = self.y - p.y
        if abs(xDiff) <= 1 and yDiff == 0 and o == "down":
            return True
        elif abs(xDiff) <= 1 and yDiff == 0 and o == "up":
            return True
        elif xDiff == 0 and abs(yDiff) <= 1 and o == "left":
            return True
        elif xDiff == 0 and abs(yDiff) <= 1 and o == "right":
            return True
        else:
            return False

    def up(self, i):
        self.y = self.y - i

    def down(self, i):
        self.y = self.y + i

    def left(self, i):
        self.x = self.x - i

    def right(self, i):
        self.x = self.x + i

    def outOfBounds(self):
        return self.x < 0 or self.x > ((WIDTH - SIZE)/ SIZE) or self.y < 0 or self.y > ((HEIGHT - SIZE)/ SIZE)

    def hitBottom(self):
        return self.y >= ((HEIGHT - SIZE) / SIZE)

    def stacked(self, p):
        return (self.x == p.x) and ((p.y - self.y) == 1)
    
#
class ship:
    def __init__(self, p, o):
        self.pos = p
        self.ori = o

    def move(self):
        eval('self.pos.' + self.ori + '(' + str(SHIP_SPEED) + ')')

    def turn(self, o):
        if o == "left":
            self.ori = "left"
        elif o == "right":
            self.ori = "right"
        elif o == "up":
            self.ori = "up"
        elif o == "down":
            self.ori = "down"

    def draw(self):
        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(self.pos.x * SIZE, self.pos.y * SIZE, SIZE, SIZE))

    def hitWall(self):
        return self.pos.outOfBounds()

    def getOri(self):
        return copy.copy(self.ori)

    def getPos(self):
        return copy.copy(self.pos)

    def against(self, t):
        for b in t.bs:
            if self.pos.against(b.pos, self.ori):
                return True

        return False

#
class fleet:
    def __init__(self, xs):
        self.ships = xs

    def move(self):
        prev_posn = self.ships[0].getPos()
        self.ships[0].move()

        for ship in self.ships[1:]:
            tmp = ship.pos
            ship.pos = prev_posn
            prev_posn = tmp

    def turn(self, o):
        self.ships[0].turn(o)

    def draw(self):
        for ship in self.ships:
            ship.draw()

    def hitWall(self):
        return self.ships[0].hitWall()

    def getOri(self):
        return self.ships[0].getOri()

    def getPos(self):
        return self.ships[0].getPos()

#
class block:
    def __init__(self, p, c):
        self.pos = p
        self.color = c

    def move(self):
        eval('self.pos.down(' + str(BLOCK_SPEED) + ')')

    def hitBottom(self):
        return self.pos.hitBottom()

    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x * SIZE, self.pos.y * SIZE, SIZE, SIZE))

    def hitAnother(self, b):
        return self.pos.stacked(b.pos)

    def push(self, ori):
        eval('self.pos.' + ori + '(' + str(SHIP_SPEED) + ')')
    
# 
class tetromino:    
    def buildTetromino(self, letter, color, topLeft):
        tetromino = []
        if letter == "O":
            tetromino.append(block(posn(topLeft, -2), color))
            tetromino.append(block(posn(topLeft, -1), color))
            tetromino.append(block(posn(topLeft + 1, -2), color))
            tetromino.append(block(posn(topLeft + 1, -1), color))
        elif letter == "I":
            tetromino.append(block(posn(topLeft, -4), color))
            tetromino.append(block(posn(topLeft, -3), color))
            tetromino.append(block(posn(topLeft, -2), color))
            tetromino.append(block(posn(topLeft, -1), color))
        elif letter == "L":
            tetromino.append(block(posn(topLeft, -3), color))
            tetromino.append(block(posn(topLeft, -2), color))
            tetromino.append(block(posn(topLeft, -1), color))
            tetromino.append(block(posn(topLeft + 1, -1), color))
        elif letter == "J":
            tetromino.append(block(posn(topLeft + 1, -3), color))
            tetromino.append(block(posn(topLeft + 1, -2), color))
            tetromino.append(block(posn(topLeft + 1, -1), color))
            tetromino.append(block(posn(topLeft, -1), color))
        elif letter == "Z":
            tetromino.append(block(posn(topLeft + 1, -3), color))
            tetromino.append(block(posn(topLeft + 1, -2), color))
            tetromino.append(block(posn(topLeft, -2), color))
            tetromino.append(block(posn(topLeft, -1), color))
        elif letter == "S":
            tetromino.append(block(posn(topLeft, -3), color))
            tetromino.append(block(posn(topLeft, -2), color))
            tetromino.append(block(posn(topLeft + 1, -2), color))
            tetromino.append(block(posn(topLeft + 1, -1), color))
        elif letter == "T":
            tetromino.append(block(posn(topLeft, -3), color))
            tetromino.append(block(posn(topLeft, -2), color))
            tetromino.append(block(posn(topLeft, -1), color))
            tetromino.append(block(posn(topLeft + 1, -2), color))

        return tetromino

    def __init__(self):
        startingX = randint(0, ((WIDTH - (SIZE * 2)) / SIZE))
        self.color = [randint(10,255), randint(10,255), randint(10,255)]
        self.stopped = False
        blockType = randint(0,6)

        if blockType == 0:
            self.bs = self.buildTetromino("O", self.color, startingX)
        elif blockType == 1:
            self.bs = self.buildTetromino("I", self.color, startingX)
        elif blockType == 2:
            self.bs = self.buildTetromino("L", self.color, startingX)
        elif blockType == 3:
            self.bs = self.buildTetromino("J", self.color, startingX)
        elif blockType == 4:
            self.bs = self.buildTetromino("Z", self.color, startingX)
        elif blockType == 5:
            self.bs = self.buildTetromino("S", self.color, startingX)
        elif blockType == 6:
            self.bs = self.buildTetromino("T", self.color, startingX)
            
    def hitBottom(self):
        for b in self.bs:
            if b.hitBottom():
                self.stopped = True
                return True

    def hitAnother(self, xs):
        for b in self.bs:
            for x in xs:
                if b.hitAnother(x):
                    self.stopped = True
                    return True

        return False
        
    def move(self):
        for b in self.bs:
            b.move()

    def draw(self):
        for b in self.bs:
            b.draw()

    def push(self, ori):
        for b in self.bs:
            b.push(ori)
            
    #def rotate(self):

def blockListify(x, ts):
    blockList = []

    for t in ts:
        if t != x:
            for b in t.bs:
                blockList.append(b)

    return blockList
    
#
class bullet:
    def __init__(self, p, o):
        self.pos = p
        self.ori = o

    def move(self):
        eval('self.pos.' + self.ori + '(' + str(BULLET_SPEED) + ')')

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(((self.pos.x * SIZE) + (SIZE / 4)), ((self.pos.y * SIZE) + (SIZE / 4)), (SIZE / 2), (SIZE / 2)))

    def isDead(self):
        return self.pos.outOfBounds()

class world:
    def __init__(self):
        ship1 = ship(posn(0,0), "down")
        self.bullets = []
        self.ts = [tetromino()]
        self.player = fleet([ship1])
        self.blockClock = -1

    def draw(self):
        self.player.draw()
        
        for bullet in self.bullets:
            bullet.draw()

        for t in self.ts:
            t.draw()

    def move(self):
        self.player.move()

        for bullet in self.bullets:
            bullet.move()

        for t in self.ts:
            if (self.player.ships[0].against(t)):
                t.push(self.player.ships[0].getOri())
            elif ((not t.hitBottom()) and (not t.hitAnother(blockListify(t, self.ts))) and self.blockClock == 0):
                t.move()
                

    def playerTurn(self, o):
        self.player.turn(o)

    def blockTick(self):
        if (self.blockClock == 3):
            self.blockClock = 0
        else:
            self.blockClock = self.blockClock + 1

    def collision(self):
        return self.player.hitWall()

    def newBullet(self):
        bOrientation = self.player.getOri()
        bPos = self.player.getPos()
        eval('bPos.' + bOrientation  + '(1)')
        self.bullets.append(bullet(bPos, bOrientation))

    def rmDeadBullets(self):
        for bullet in self.bullets:
            if bullet.isDead():
                self.bullets.remove(bullet)

    def addTetromino(self):
        for t in self.ts:
            if (not t.stopped):
                return

        self.ts.append(tetromino())

# Create world
theWorld = world()
gameOver = False

while not gameOver:
    clock.tick(TICK)
    theWorld.blockTick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: theWorld.playerTurn("up")
            elif event.key == pygame.K_DOWN: theWorld.playerTurn("down")
            elif event.key == pygame.K_LEFT: theWorld.playerTurn("left")
            elif event.key == pygame.K_RIGHT: theWorld.playerTurn("right")
            elif event.key == pygame.K_SPACE: theWorld.newBullet()

    if theWorld.collision():
        gameOver = True
    else:
        # Remove dead bullets
        theWorld.rmDeadBullets()
        theWorld.addTetromino()
        
        screen.fill((0,0,0))
        theWorld.move()
        theWorld.draw()    

    pygame.display.flip()

pygame.quit()
quit()
