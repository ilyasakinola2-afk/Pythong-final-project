# Week 9 starter: Platformer - A Complete Level
#
# This is your Week 8 platformer. Today's answers are already here, hidden in comments.
# When the slide says "uncomment Exercise N":
#   1. Find every block between "EXERCISE N" and "end EXERCISE N" (Cmd+F / Ctrl+F helps).
#   2. Select the lines inside the block and press Cmd + /  (Windows: Ctrl + /).
#   3. Lines tagged "EXERCISE N: comment this out" are the old version.
#      Select them and press Cmd + / too.
#   4. Run the file.
# Exercise 4 has no block: you type it yourself.
#
# Keep the "images" folder next to this file.
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer — A Complete Level")
clock = pygame.time.Clock()
# ===== EXERCISE 3 =====
font = pygame.font.Font(None, 48)
# ===== end EXERCISE 3 =====

GRAVITY = 3600
JUMP = -900
MOVE = 300
START_POS = (80, 520)
# ===== EXERCISE 5 =====
LEVEL_WIDTH = 1600
# ===== end EXERCISE 5 =====


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, groups):
        super().__init__(groups)
        self.image = pygame.Surface((w, h))
        self.image.fill("sienna")
        self.rect = self.image.get_frect(topleft=(x, y))
# =====
class Goal(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        # self.image = pygame.Surface((28, 48))  # EXERCISE 7: comment this out
        # self.image.fill("limegreen")  # EXERCISE 7: comment this out
        # ===== EXERCISE 7 =====
        self.image = pygame.image.load("images/flag.png")
        # ===== end EXERCISE 7 =====
        self.rect = self.image.get_frect(midbottom=pos)
# ===== end EXERCISE 2 =====


# ===== EXERCISE 6 =====
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - WIDTH / 2)

        for sprite in self:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
# ===== end EXERCISE 6 =====


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, platforms):
        super().__init__(groups)
        # self.image = pygame.Surface((40, 60))  # EXERCISE 7: comment this out
        # self.image.fill("dodgerblue")  # EXERCISE 7: comment this out
        # ===== EXERCISE 7 =====
        # self.image = pygame.image.load("images/player/0.png")  # EXERCISE 8: comment this out
        # ===== end EXERCISE 7 =====
        # ===== EXERCISE 8 =====
        self.frames = [
            pygame.image.load("images/player/0.png"),
            pygame.image.load("images/player/1.png"),
            pygame.image.load("images/player/2.png"),
        ]
        self.frame_index = 0
        self.flip = False
        self.image = self.frames[0]
        # ===== end EXERCISE 8 =====
        self.rect = self.image.get_frect(midbottom=pos)
        self.direction = pygame.Vector2()
        self.on_floor = False
        self.platforms = platforms

    def update(self, dt):
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
            if self.direction.y >= 0:
                self.rect.bottom = platform.rect.top
                self.direction.y = 0
                self.on_floor = True

        # W8 Mini Challenge 2: stay inside the window
        self.rect.x = max(0, min(self.rect.x, LEVEL_WIDTH - self.rect.width))
        # ===== EXERCISE 8 =====
        self.animate(dt)
        # ===== end EXERCISE 8 =====

    # ===== EXERCISE 8 =====
    def animate(self, dt):
        if self.direction.x:
            self.frame_index += 10 * dt
            self.flip = self.direction.x < 0
        else:
            self.frame_index = 0
        if not self.on_floor:
            self.frame_index = 1
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flip, False)
    # ===== end EXERCISE 8 =====


# all_sprites = pygame.sprite.Group()  # EXERCISE 6: comment this out
# ===== EXERCISE 6 =====
all_sprites = AllSprites()
# ===== end EXERCISE 6 =====
platforms = pygame.sprite.Group()
# ===== EXERCISE 2 =====
goals = pygame.sprite.Group()
# ===== end EXERCISE 2 =====

# Platform(0, 520, WIDTH, 80, (all_sprites, platforms))  # EXERCISE 1: comment this out
# ===== EXERCISE 1 =====
Platform(0, 520, 360, 80, (all_sprites, platforms))  # ground - now shorter
Platform(250, 430, 170, 24, (all_sprites, platforms))  # middle
Platform(500, 340, 170, 24, (all_sprites, platforms))  # high
# ===== end EXERCISE 1 =====
# ===== EXERCISE 5 =====
Platform(760, 420, 160, 24, (all_sprites, platforms))  # past the window
Platform(1000, 360, 160, 24, (all_sprites, platforms))  # past the window
Platform(1240, 300, 200, 24, (all_sprites, platforms))  # past the window
# ===== end EXERCISE 5 =====
# ===== EXERCISE 2 =====
# Goal((585, 340), (all_sprites, goals))  # EXERCISE 5: comment this out

# ===== end EXERCISE 2 =====
# ===== EXERCISE 5 =====
Goal((1400, 300), (all_sprites, goals))  # the flag moves to the far end
# ===== end EXERCISE 5 =====
player = Player(START_POS, all_sprites, platforms)

# ===== EXERCISE 3 =====
state = "playing"
# ===== end EXERCISE 3 =====

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Exercise 4 (you type it): only update the game while state is "playing"
    if state == "playing":
        all_sprites.update(dt)

        # ===== EXERCISE 3 =====
        if pygame.sprite.spritecollide(player, goals, False):
            state = "win"
        if player.rect.top > HEIGHT:
            state = "lose"
        # ===== end EXERCISE 3 =====

    screen.fill("skyblue")
    # all_sprites.draw(screen)  # EXERCISE 6: comment this out
    # ===== EXERCISE 6 =====
    all_sprites.draw(player.rect.center)
    # ===== end EXERCISE 6 =====
    # ===== EXERCISE 3 =====
    if state == "win":
        screen.blit(font.render("You win!", True, "white"), (300, 40))
    elif state == "lose":
        screen.blit(font.render("You lose!", True, "white"), (300, 40))
    # ===== end EXERCISE 3 =====
    pygame.display.update()

pygame.quit()
