# Migraine

import pygame
import random

WINDOW = (500,700)

pygame.init()

gameDisplay = pygame.display.set_mode(WINDOW)
pygame.display.set_caption('Migraine')

pygame.display.update()

gameExit = False

while not gameExit:
    for event in pygame.event.get():
        print(event)

pygame.quit()
quit()




