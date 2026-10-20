import random

import pygame


WIDTH = 800
HEIGHT = 400

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")


class Pong(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill("white")
        self.rect = self.image.get_frect(center=(x, y))
        self.velocity = pygame.Vector2(200, -150)

    def update(self, dt):
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity.y = abs(self.velocity.y)
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity.y = -abs(self.velocity.y)

        if self.rect.right < 0:
            return 2
        if self.rect.left > WIDTH:
            return 1

    def reset(self, direction=None):
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        horizontal_direction = direction or random.choice((-1, 1))
        self.velocity = pygame.Vector2(
            300 * horizontal_direction,
            random.choice((-220, 220)),
        )

    def bounce_off_paddle(self, paddle):
        if not self.rect.colliderect(paddle.rect):
            return

        if self.velocity.x < 0:
            self.rect.left = paddle.rect.right
            self.velocity.x = abs(self.velocity.x)
        elif self.velocity.x > 0:
            self.rect.right = paddle.rect.left
            self.velocity.x = -abs(self.velocity.x)


class Player1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 50))
        self.image.fill("white")
        self.rect = self.image.get_frect(topleft=(x, y))
        self.speed = 250

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.rect.y += self.speed * dt
        # if keys[pygame.K_a]:
        #     self.rect.x -= self.speed * dt
        # if keys[pygame.K_d]:
        #     self.rect.x += self.speed * dt

        self.rect.clamp_ip(screen.get_rect())


class Player2(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((15, 50))
        self.image.fill(color)
        self.rect = self.image.get_frect(topleft=(x, y))
        self.speed = 250

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed * dt
        # if keys[pygame.K_LEFT]:
        #     self.rect.x -= self.speed * dt
        # if keys[pygame.K_RIGHT]:
        #     self.rect.x += self.speed * dt

        self.rect.clamp_ip(screen.get_rect())


pongs = pygame.sprite.Group()
pong = Pong(WIDTH / 2, HEIGHT / 2)
pongs.add(pong)

players1 = pygame.sprite.Group()
player1 = Player1(x= 20, y = HEIGHT /2,  )
players1.add(player1)

players2 = pygame.sprite.Group()
player2 = Player2(x = 780, y = HEIGHT/ 2,color = "white")
players2.add(player2)


TITLE_FONT = pygame.font.Font(None, 72)
TEXT_FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 26)
WINNING_SCORE = 5

game_state = "start"
player1_score = 0
player2_score = 0
winner = None


def draw_centered(text, font, y, color="white"):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH / 2, y))
    screen.blit(text_surface, text_rect)


def draw_game():
    screen.fill((30, 30, 40))
    pygame.draw.line(screen, (100, 100, 110), (WIDTH / 2, 0), (WIDTH / 2, HEIGHT), 2)
    draw_centered(f"{player1_score}        {player2_score}", TITLE_FONT, 45)
    pongs.draw(screen)
    players1.draw(screen)
    players2.draw(screen)


def draw_start_screen():
    screen.fill((30, 30, 40))
    draw_centered("PONG", TITLE_FONT, 85)
    draw_centered("Press SPACE to start", TEXT_FONT, 175)
    draw_centered("Player 1: W / S", SMALL_FONT, 250)
    draw_centered("Player 2: UP / DOWN", SMALL_FONT, 285)
    draw_centered(f"First to {WINNING_SCORE} wins", SMALL_FONT, 335, "lightgray")


def draw_end_screen():
    screen.fill((30, 30, 40))
    draw_centered(f"Player {winner} wins!", TITLE_FONT, 95)
    draw_centered(f"Final score: {player1_score} - {player2_score}", TEXT_FONT, 180)
    draw_centered("Press R to play again", TEXT_FONT, 270)
    draw_centered("Press ESC to quit", SMALL_FONT, 325, "lightgray")


running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif game_state == "start" and event.key == pygame.K_SPACE:
                player1_score = 0
                player2_score = 0
                winner = None
                pong.reset()
                game_state = "playing"
            elif game_state == "game_over" and event.key == pygame.K_r:
                player1_score = 0
                player2_score = 0
                winner = None
                pong.reset()
                game_state = "playing"

    if game_state == "playing":
        players1.update(dt)
        players2.update(dt)
        scorer = pong.update(dt)
        pong.bounce_off_paddle(player1)
        pong.bounce_off_paddle(player2)

        if scorer == 1:
            player1_score += 1
        elif scorer == 2:
            player2_score += 1

        if scorer:
            if player1_score >= WINNING_SCORE or player2_score >= WINNING_SCORE:
                winner = scorer
                game_state = "game_over"
            else:
                pong.reset(direction=1 if scorer == 1 else -1)

        draw_game()
    elif game_state == "start":
        draw_start_screen()
    else:
        draw_end_screen()

    pygame.display.flip()


pygame.quit()
