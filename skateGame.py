import pygame
from pygame.locals import *
from sys import exit

width = 640
height = 480

white = (255, 255, 255)

window = pygame.display.set_mode((width, height))

pygame.display.set_caption('T-Skate Game')

clock = pygame.time.Clock()
while True:
    clock.tick(30)
    window.fill(white)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    pygame.display.flip()
