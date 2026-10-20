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

        self.rect = self.image.get_rect(center = (x,y))
        self.speed = 2
    def update(self,dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        self.rect.clamp_ip(screen.get_rect())

players1 = pygame.sprite.Group()
player1 = Player1(x=50,y=50)
players1.add(player1)


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
    player1.update(dt)
    players1.draw(screen)
    pygame.display.flip()
    pygame.display.update()


pygame.quit()