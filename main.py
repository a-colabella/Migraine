
# Migraine
# An arcade game that combines elements of
# snake, tetris, space invaders, potentially more?
import pygame
import random

# Initialize
pygame.init()

# Display
winfo = pygame.display.Info()
screen = pygame.display.set_mode((winfo.current_w / 2, winfo.current_h))
clock = pygame.time.Clock()

# Caption
pygame.display.set_caption('Migraine')
pygame.display.update()

class posn:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def equals(self, p):
        return self.x == p.x and self.y == p.y

    def up(self):
        self.y = self.y - 1

    def down(self):
        self.y = self.y + 1

    def left(self):
        self.x = self.x - 1

    def right(self):
        self.x = self.x + 1
    
#
class ship:
    def __init__(self, p, o):
        self.pos = p
        self.ori = o

    def move(self):
        eval('self.pos.' + self.ori + '()')

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
        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(self.pos.x * 50, self.pos.y * 50, 50, 50))

#
class fleet:
    def __init__(self, xs):
        self.ships = xs

    def move(self):
        prev_posn = self.ships[0].pos
        self.ships[0].move()

        for ship in self.ships[1:]:
            tmp = ship.pos
            ship.pos = prev_posn
            prev_posn = tmp

    def draw(self):
        for ship in self.ships:
            ship.draw()

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
        eval('self.pos.' + self.ori + '()')

class world:
    def __init__(self):
        ship1 = ship(posn(0,0), "down")
        self.bullets = []
        self.ts = []
        self.player = fleet([ship1])

    def draw(self):
        self.player.draw()

    def move(self):
        self.player.move()

# Create world
theWorld = world()
gameExit = False

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

    screen.fill((0,0,0))
    theWorld.move()
    theWorld.draw()
    pygame.display.flip()
    clock.tick(1)
        

pygame.quit()
quit()
