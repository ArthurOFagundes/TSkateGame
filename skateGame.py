from difflib import restore
import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange

pygame.init()
pygame.mixer.init()

main_directory = os.path.dirname(__file__)
images_directory = os.path.join(main_directory, "images")
sounds_directory = os.path.join(main_directory, "sounds")

width = 640
height = 480

white = (255, 255, 255)
black = (0, 0, 0)

window = pygame.display.set_mode((width, height))

pygame.display.set_caption('T-Skate Game')
gameIcon = pygame.image.load(os.path.join(images_directory, "TskateIcon.png"))
pygame.display.set_icon(gameIcon)

sprite_sheet = pygame.image.load(os.path.join(
    images_directory, "skateSpriteSheet.png")).convert_alpha()

collision_sound = pygame.mixer.Sound(
    os.path.join(sounds_directory, "death_sound.wav"))
collision_sound.set_volume(1)

point_sound = pygame.mixer.Sound(os.path.join(sounds_directory, "score_sound.wav"))
point_sound.set_volume(1)

collided = False

points = 0

game_velocity = 10

def mensage_show(msg, size, color):
    font = pygame.font.SysFont("comicsanssms", size, True, False)
    mensage = f"{msg}"
    text_formatted = font.render(mensage, False, color)
    return text_formatted

def restart_game():
    global points, game_velocity, collided
    points = 0
    game_velocity = 10
    collided = False
    barrier.rect.x = width
    skateboard.rect.y = height - 31 - 48
    skateboard.ollie = False

class Skate(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ollie_sound = pygame.mixer.Sound(
            os.path.join(sounds_directory, "ollie_sound.wav"))
        self.ollie_sound.set_volume(1)
        self.skateboard_image = []
        self.img = sprite_sheet.subsurface((0, 0), (32, 32))
        self.img = pygame.transform.scale(self.img, (96, 96))
        self.skateboard_image.append(self.img)

        self.index_list = 0
        self.image = self.skateboard_image[self.index_list]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_init = height - 31 - 48
        self.rect.center = (100, height - 32)
        self.ollie = False

    def doOllie(self):
        self.ollie = True
        self.ollie_sound.play()

    def update(self):
        if self.ollie == True:
            if self.rect.y <= 300:
                self.ollie = False
            self.rect.y -= 15
        else:
            if self.rect.y < self.pos_y_init:
                self.rect.y += 10
            else:
                self.rect.y = self.pos_y_init


class Clounds(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((96, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (96, 96))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = width - randrange(32, 320, 92)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = width
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= game_velocity


class Streets(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((64, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (96, 96))
        self.rect = self.image.get_rect()
        self.rect.y = height - 64
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = width
        self.rect.x -= game_velocity


class Barrier(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*4, 32*4))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (width, height - 40)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = width
        self.rect.x -= game_velocity


all_sprites = pygame.sprite.Group()
skateboard = Skate()
all_sprites.add(skateboard)

for i in range(4):
    clound = Clounds()
    all_sprites.add(clound)

for i in range(12):
    street = Streets(i)
    all_sprites.add(street)

barrier = Barrier()
all_sprites.add(barrier)

obstacle_group = pygame.sprite.Group()
obstacle_group.add(barrier)

clock = pygame.time.Clock()
while True:
    clock.tick(30)
    window.fill(white)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                if skateboard.rect.y != skateboard.pos_y_init or collided == True:
                    pass
                else:
                    skateboard.doOllie()

            if event.key == K_r and collided == True:
                restart_game()

    collisions = pygame.sprite.spritecollide(
        skateboard, obstacle_group, False, pygame.sprite.collide_mask)

    all_sprites.draw(window)

    if collisions and collided == False:
        collision_sound.play()
        collided = True
        pass

    if collided == True:
        if points % 100 == 0:
            points += 1
        
        game_over = mensage_show("GAME OVER", 40, black)
        window.blit(game_over,(width//2 - 105, height//2.5))

        death_points = mensage_show(f"Voc?? morreu com: {points}", 30, black)
        window.blit(death_points, (width//2 - 130, height//2.5 + 60))

        restart_mensage = mensage_show('Pressione R para dar restart', 20, black)
        window.blit(restart_mensage, (width//2 - 110 , height//2.5 + 120))

    else:
        points += 1
        all_sprites.update()
        points_view = mensage_show(f"Pontos: {points}", 40, black)
        window.blit(points_view, (420, 30))


    if points % 100 == 0:
        point_sound.play()

        if game_velocity >= 23:
            game_velocity += 0
        else:
            game_velocity += 1

    pygame.display.flip()
