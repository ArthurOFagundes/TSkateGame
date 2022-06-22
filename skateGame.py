import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange

main_directory = os.path.dirname(__file__)
images_directory = os.path.join(main_directory, "images")
sounds_dorectory = os.path.join(main_directory, "sounds")

width = 640
height = 480

white = (255, 255, 255)

window = pygame.display.set_mode((width, height))

pygame.display.set_caption('T-Skate Game')

sprite_sheet = pygame.image.load(os.path.join(
    images_directory, "skateSpriteSheet.png")).convert_alpha()


class Skate(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.skateboard_image = []
        self.img = sprite_sheet.subsurface((0, 0), (32, 32))
        self.img = pygame.transform.scale(self.img, (32*3, 32*3))
        self.skateboard_image.append(self.img)

        self.index_list = 0
        self.image = self.skateboard_image[self.index_list]
        self.rect = self.image.get_rect()
        self.rect.center = (100, height - 32)


class Clounds(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((3*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = width - randrange(32, 320, 92)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = width
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= 10


class Streets(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((2*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.y = height - 64
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = width
        self.rect.x -= 10


all_sprites = pygame.sprite.Group()
skateboard = Skate()
all_sprites.add(skateboard)

for i in range(4):
    clound = Clounds()
    all_sprites.add(clound)

for i in range(12):
    street = Streets(i)
    all_sprites.add(street)

clock = pygame.time.Clock()
while True:
    clock.tick(30)
    window.fill(white)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    all_sprites.draw(window)
    all_sprites.update()

    pygame.display.flip()
