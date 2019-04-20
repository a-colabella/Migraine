# Migraine
# An arcade game that combines elements of
# snake, tetris, space invaders, potentially more?
import pygame
import random
import copy

SIZE = 50
TICK = 10

# Initialize
pygame.init()

# Display
winfo = pygame.display.Info()
#WIDTH, HEIGHT = (winfo.current_w / 2, winfo.current_h)
WIDTH, HEIGHT = (950, 950)
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

    def collision(self, p):
        return self.x == p.x and self.y == p.y

    def up(self, i):
        self.y = self.y - i

    def down(self, i):
        self.y = self.y + i

    def left(self, i):
        self.x = self.x - i

    def right(self, i):
        self.x = self.x + i

    def outOfBounds(self):
        return self.x < 0 or self.x > ((WIDTH - 100)/ 50) or self.y < 0 or self.y > ((HEIGHT - 100)/ 50)
    
#
class ship:
    def __init__(self, p, o):
        self.pos = p
        self.ori = o

    def move(self):
        eval('self.pos.' + self.ori + '(1)')

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

# 
class tetromino:
    def __init__(self, p, o, s):
        self.ori = o
        self.shape = t

    def turn(self, o):
        if o == "left":
            self.ori = "left"
        elif o == "right":
            self.ori = "right"
        elif o == "up":
            self.ori = "up"
        elif o == "down":
            self.ori = "down"

#
class bullet:
    def __init__(self, p, o):
        self.pos = p
        self.ori = o

    def move(self):
        eval('self.pos.' + self.ori + '(2)')

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(((self.pos.x * SIZE) + (SIZE / 4)), ((self.pos.y * SIZE) + (SIZE / 4)), (SIZE / 2), (SIZE / 2)))

    def isDead(self):
        return self.pos.outOfBounds()

    

class world:
    def __init__(self):
        ship1 = ship(posn(0,0), "down")
        self.bullets = []
        self.ts = []
        self.player = fleet([ship1])

    def draw(self):
        self.player.draw()
        
        for bullet in self.bullets:
            bullet.draw()

    def move(self):
        self.player.move()

        for bullet in self.bullets:
            bullet.move()

    def playerTurn(self, o):
        self.player.turn(o)

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

# Create world
theWorld = world()
gameOver = False

while not gameOver:
    clock.tick(TICK)
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
        
        screen.fill((0,0,0))
        theWorld.move()
        theWorld.draw()    

    pygame.display.flip()

pygame.quit()
quit()
