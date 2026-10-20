import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer — Gravity and Jump")
clock = pygame.time.Clock()

GRAVITY = 3600 #could be simulated as the amonunt of gravity due to the planet ur on
JUMP = -960 #could be simulated as the vertical jump of a person
MOVE = 300

class Player(pygame.sprite.Sprite):
    def __init__(self, pos , groups ,platforms):
        super().__init__(groups)
        self.image = pygame.Surface((40,60))
        self.image.fill("dodgerblue")
        self.rect = self.image.get_rect(midbottom=pos)
        self.platforms = platforms
        self.direction = pygame.Vector2()
        self.on_floor = False


    def update(self,dt ):

        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.rect.x += self.direction.x * MOVE * dt

        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = JUMP


        self.direction.y += GRAVITY * dt
        self.rect.y += self.direction.y * dt

        self.on_floor = False
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        for platform in hits:
            if self.direction.y > 0:
                self.rect.bottom = platform.rect.top
                self.on_floor = True
                self.direction.y = 0

        self.rect.clamp_ip(screen.get_rect())



class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y, w,h, groups):
        super().__init__(groups)
        self.image = pygame.Surface((w,h))
        self.image.fill("sienna")
        self.rect = self.image.get_rect(topleft=(x,y))





all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

player = Player((120,300), all_sprites , platforms)
Platform(0,520 ,WIDTH , 80 ,( all_sprites, platforms))

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update(dt)

    screen.fill("skyblue")
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()

#still need to learn how the collision works and how to determine when 2 sprites are colliding