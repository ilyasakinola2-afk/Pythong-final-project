# make a map and the 2 player classes map must have obstacles
# add a menu to pick either 2 player or 1 player
# make random drops anywhere on the map( shield for 5 seconds, faster amo and increased speed)
# when one player is picked use a bot so I need to know how to make a bot
# add increasing difficulties
# make an end menu

import pygame
from random import randint

WIDTH = 1200
HEIGHT = 600
PLAYER1_SPEED = 2
PLAYER2_SPEED = 2
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TANK SHOOTERS"
                           "")


class Player1(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.original_image = pygame.image.load("assets/PNG/Tanks/tankRed.png")
        self.image = self.original_image
        self.angle = 0
        self.rect = self.image.get_rect(center = (x,y))
        self.speed = PLAYER1_SPEED



        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed


        if keys[pygame.K_w]:
            new_angle = 180
        if keys[pygame.K_s]:
            new_angle = 0
        if keys[pygame.K_a]:
            new_angle = -90
        if keys[pygame.K_d]:
            new_angle = 90



        if keys[pygame.K_w]:
            newer_angle = 180
        if keys[pygame.K_s]:
            newer_angle = 0
        if keys[pygame.K_a]:
            newer_angle = -90
        if keys[pygame.K_d]:
            newer_angle = 90



        if new_angle != self.angle:
            center = self.rect.center
            self.angle = new_angle
            self.image = pygame.transform.rotate(self.original_image, new_angle)
            self.rect=self.image.get_rect(center = center)

        self.rect.clamp_ip(screen.get_rect())


class Barrel1(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.original_image = pygame.image.load("assets/PNG/Barrels/BarrelRed.png")
        self.image = self.original_image
        self.angle = 0
        self.rect = self.image.get_rect(center = (x,y))
    def update(self,dt):
        keys = pygame.key.get_pressed()
        new_angle = self.angle

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_w]:
            newer_angle = 180
        if keys[pygame.K_s]:
            newer_angle = 0
        if keys[pygame.K_a]:
            newer_angle = -90
        if keys[pygame.K_d]:
            newer_angle = 90

        if new_angle != self.angle:
            center = self.rect.center
            self.angle = new_angle
            self.image = pygame.transform.rotate(self.original_image, new_angle)
            self.rect = self.image.get_rect(center=center)

        self.rect.clamp_ip(screen.get_rect())


class Player2(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.original_image = pygame.image.load("assets/PNG/Tanks/tankBlue.png")
        self.image = self.original_image
        self.angle = 0
        self.rect = self.image.get_rect(center = (x,y))
        self.speed = PLAYER2_SPEED

    def update(self,dt):

        keys = pygame.key.get_pressed()
        new_angle = self.angle
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        if keys[pygame.K_LEFT]:
            new_angle = -90
        if keys[pygame.K_RIGHT]:
            new_angle = 90
        if keys[pygame.K_UP]:
            new_angle = 180
        if keys[pygame.K_DOWN]:
            new_angle = 0

        if new_angle != self.angle:
            center = self.rect.center
            self.angle = new_angle
            self.image = pygame.transform.rotate(self.original_image, new_angle)
            self.rect=self.image.get_rect(center = tank.rect.center)










all_sprites = pygame.sprite.Group()
players2 = pygame.sprite.Group()
player2 = Player2(x=150,y=150)
players2.add(player2)




players1 = pygame.sprite.Group()
player1 = Player1(x=50,y=50)
players1.add(player1)

barrels1 = pygame.sprite.Group()
barrel1 = Barrel1(x=50,y=50)
barrels1.add(barrel1)

all_sprites.add(players1,players2,barrel1)


fullscreen = False
running = True
while running:
    dt = clock.tick(60)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            fullscreen = not fullscreen

            if fullscreen:
                screen = pygame.display.set_mode(
                    (0, 0),
                    pygame.FULLSCREEN
                )
            else:
                screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill("Blue")
    all_sprites.update(dt)
    all_sprites.draw(screen)
    pygame.display.flip()
    pygame.display.update()


pygame.quit()