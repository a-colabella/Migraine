# Migraine
# An arcade game that combines elements of
# snake, tetris, space invaders, potentially more?
import pygame
from random import randint
import copy

WIDTH, HEIGHT = (500, 950)
SIZE = 25
TICK = 10
BLOCK_SPEED = 1
SHIP_SPEED = 1
BULLET_SPEED = 1

class Posn:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

    def walled(self, o):
        return (self.x == 0 and o == "left") or (self.x == ((WIDTH - SIZE) / SIZE) and o == "right") or (self.y == ((HEIGHT - SIZE) / SIZE) and o == "down")

    def against(self, p, o):
        xDiff = self.x - p.x
        yDiff = self.y - p.y
        if xDiff == 0 and yDiff == 0 and o == "down":
            return True
        elif xDiff == 0 and yDiff == 0 and o == "up":
            return True
        elif xDiff == 0 and yDiff == 0 and o == "left":
            return True
        elif xDiff == 0 and yDiff == 0 and o == "right":
            return True
        else:
            return False

class Ship:
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

    def outOfBounds(self):
        return self.pos.outOfBounds()

    def hitStoppedPiece(self, ts):
        for t in ts:
            if (self.against(t) and t.stopped):
                return True

        return False

    def getOri(self):
        return copy.copy(self.ori)

    def getPos(self):
        return copy.copy(self.pos)

    def against(self, t):
        for b in t.bs:
            if self.pos.against(b.pos, self.ori):
                return True

        return False

class Block:
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

    def walled(self, o):
        return self.pos.walled(o)

    def push(self, ori):
        eval('self.pos.' + ori + '(' + str(SHIP_SPEED) + ')')

class Tetromino:
    letters = ["O", "I", "S", "Z", "L", "J", "T"]
    shapes = {
        "O": [[[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]],
            [[0,1,1,0], [0,1,1,0], [0,1,1,0], [0,1,1,0]],
            [[0,1,1,0], [0,1,1,0], [0,1,1,0], [0,1,1,0]],
            [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]],

        "I": [[[0,0,0,0], [0,0,1,0], [0,0,0,0], [0,0,1,0]],
            [[1,1,1,1], [0,0,1,0], [1,1,1,1], [0,0,1,0]],
            [[0,0,0,0], [0,0,1,0], [0,0,0,0], [0,0,1,0]],
            [[0,0,0,0], [0,0,1,0], [0,0,0,0], [0,0,1,0]]],

        "S": [[[0,0,0,0], [0,0,1,0], [0,0,0,0], [0,0,1,0]],
            [[0,0,1,1], [0,0,1,1], [0,0,1,1], [0,0,1,1]],
            [[0,1,1,0], [0,0,0,1], [0,1,1,0], [0,0,0,1]],
            [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]],

        "Z": [[[0,0,0,0], [0,0,0,1], [0,0,0,0], [0,0,0,1]],
            [[0,1,1,0], [0,0,1,1], [0,1,1,0], [0,0,1,1]],
            [[0,0,1,1], [0,0,1,0], [0,0,1,1], [0,0,1,0]],
            [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]],

        "L": [[[0,0,0,0], [0,0,5,0], [0,0,0,5], [0,5,5,0]],
            [[0,5,5,5], [0,0,5,0], [0,5,5,5], [0,0,5,0]],
            [[0,5,0,0], [0,0,5,5], [0,0,0,0], [0,0,5,0]],
            [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]],

        "J": [[[0,0,0,0], [0,0,1,1], [0,1,0,0], [0,0,1,0]],
            [[0,1,1,1], [0,0,1,0], [0,1,1,1], [0,0,1,0]],
            [[0,0,0,1], [0,0,1,0], [0,0,0,0], [0,1,1,0]],
            [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]],

        "T": [[[0,0,0,0], [0,0,1,0], [0,0,1,0], [0,0,1,0]],
            [[0,1,1,1], [0,0,1,1], [0,1,1,1], [0,1,1,0]],
            [[0,0,1,0], [0,0,1,0], [0,0,0,0], [0,0,1,0]],
            [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]]
    };

    def buildHelper(self, xs, color, topLeftX, topLeftY):
        tetromino = []

        for i in range(0, len(xs)):
            for j in range (0, len(xs[i])):
                if xs[i][j] == 1:
                    tetromino.append(Block(Posn(topLeftX + j, topLeftY + i), color))

        return tetromino
        
        
    def build(self, letter, color, topLeftX, topLeftY, rot):
        helper = []
        helper.append(self.shapes[letter][0][rot])
        helper.append(self.shapes[letter][1][rot])
        helper.append(self.shapes[letter][2][rot])
        helper.append(self.shapes[letter][3][rot])

        return self.buildHelper(helper, color, topLeftX, topLeftY)

    def __init__(self):
        startingX = randint(0, ((WIDTH - (SIZE * 4)) / SIZE))
        startingY = -3
        self.color = [randint(10,255), randint(10,255), randint(10,255)]
        self.stopped = False
        self.blockType = self.letters[randint(0,6)]
        self.rotation = 0
        self.bs = self.build(self.blockType, self.color, startingX, startingY, self.rotation)
            
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

    def walled(self, o):
        for b in self.bs:
            if b.walled(o):
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


def blockListify(x, ts):
    blockList = []

    for t in ts:
        if t != x:
            for b in t.bs:
                blockList.append(b)

    return blockList

#
class Bullet:
    def __init__(self, p, o):
        self.pos = p
        self.ori = o

    def move(self):
        eval('self.pos.' + self.ori + '(' + str(BULLET_SPEED) + ')')

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(((self.pos.x * SIZE) + (SIZE / 4)), ((self.pos.y * SIZE) + (SIZE / 4)), (SIZE / 2), (SIZE / 2)))

    def isDead(self):
        return self.pos.outOfBounds()

class World:
    def __init__(self):
        self.bullets = []
        self.ts = [Tetromino()]
        self.player = [Ship(Posn(0,0), "down")]
        self.blockClock = 0
        self.snakeClock = 0

    def draw(self):
        for x in self.player:
            x.draw()

        for bullet in self.bullets:
            bullet.draw()

        for t in self.ts:
            t.draw()

    def move(self):
        if (self.snakeClock == 0):
            self.player[0].move()

        for bullet in self.bullets:
            bullet.move()

        for t in self.ts:
            if (not t.stopped):
                if (self.player[0].against(t)):
                    if (t.walled(self.player[0].getOri())):
                        t.stopped = True
                    else:
                        t.push(self.player[0].getOri())
                elif ((not t.hitBottom()) and (not t.hitAnother(blockListify(t, self.ts))) and self.blockClock == 0):
                    t.move()

    def playerTurn(self, o):
        self.player[0].turn(o)

    def blockTick(self):
        if (self.blockClock == 7):
            self.blockClock = 0
        else:
            self.blockClock = self.blockClock + 1

        if (self.snakeClock == 1):
            self.snakeClock = 0
        else:
            self.snakeClock = 1

    def dead(self):
        return (self.player[0].outOfBounds() or self.player[0].hitStoppedPiece(self.ts))

    def shoot(self):
        bOrientation = self.player[0].getOri()
        bPos = self.player[0].getPos()
        eval('bPos.' + bOrientation  + '(1)')
        self.bullets.append(Bullet(bPos, bOrientation))

    def removeBullet(self):
        for bullet in self.bullets:
            if bullet.isDead():
                self.bullets.remove(bullet)

    def addTetromino(self):
        for t in self.ts:
            if (not t.stopped):
                return

        self.ts.append(Tetromino())

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class App:
    def __init__(self):
        pygame.init()
        winfo = pygame.display.Info()
        self.clock = pygame.time.Clock()
        self.world = World()
        self.gameOver = False
        pygame.display.set_caption('Migraine')
        pygame.display.update()

    def quit(self):
        pygame.quit()
        quit()

    def cleanUp(self):
        self.world.removeBullet()

    def go(self):
        while not self.gameOver:
            self.clock.tick(TICK)
            self.world.blockTick()

            if self.world.dead():
                self.gameOver = True

            self.cleanUp()

            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[pygame.K_RIGHT]):
                self.world.playerTurn("right")
            if (keys[pygame.K_LEFT]):
                self.world.playerTurn("left")
            if (keys[pygame.K_UP]):
                self.world.playerTurn("up")
            if (keys[pygame.K_DOWN]):
                self.world.playerTurn("down")
            if (keys[pygame.K_SPACE]):
                self.world.shoot()
            if (keys[pygame.K_ESCAPE]):
                self.gameOver = True

            
            self.world.addTetromino()
            self.world.move()
            screen.fill((0,0,0))
            self.world.draw()
            pygame.display.flip()


if __name__ == "__main__":
    theApp = App()
    theApp.go()
