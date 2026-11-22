
import math
import random

import pygame


WIDTH = 1200
HEIGHT = 700
FPS = 60
MAX_HEALTH = 3
POWERUP_DURATION = 5.0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Shooters")
clock = pygame.time.Clock()

FONT_SMALL = pygame.font.Font(None, 24)
FONT_MEDIUM = pygame.font.Font(None, 34)
FONT_LARGE = pygame.font.Font(None, 64)
FONT_TITLE = pygame.font.Font(None, 92)

WHITE = (245, 245, 245)
INK = (14, 22, 30)
DARK_PANEL = (12, 25, 36)
CYAN = (57, 218, 223)
GOLD = (255, 197, 75)
RED = (238, 77, 78)
GREEN = (104, 226, 142)
BLUE = (72, 167, 245)
PURPLE = (184, 120, 255)


def load_image(relative_path, size=None):
    image = pygame.image.load("assets/PNG/" + relative_path).convert_alpha()
    if size is not None:
        image = pygame.transform.smoothscale(image, size)
    return image


def draw_text(surface, text, font, color, center):
    rendered = font.render(text, True, color)
    surface.blit(rendered, rendered.get_rect(center=center))


GRASS = load_image("Environment/grass.png", (64, 64))
TANK_IMAGES = {
    "red": load_image("Tanks/tankRed.png", (58, 58)),
    "blue": load_image("Tanks/tankBlue.png", (58, 58)),
}
BARREL_IMAGES = {
    "red": load_image("Tanks/barrelRed.png", (22, 48)),
    "blue": load_image("Tanks/barrelBlue.png", (22, 48)),
}
BULLET_IMAGES = {
    "red": load_image("Bullets/bulletRed.png", (18, 18)),
    "blue": load_image("Bullets/bulletBlue.png", (18, 18)),
}
OBSTACLE_IMAGES = {
    "tree": load_image("Environment/treeLarge.png", (72, 72)),
    "bag": load_image("Obstacles/sandbagBrown.png", (94, 44)),
    "barrel": load_image("Obstacles/barrelGrey_side.png", (46, 46)),
    "crate": load_image("Obstacles/sandbagBeige.png", (70, 38)),
}

def facing_components(angle):
    radians = math.radians(angle)
    return math.sin(radians), math.cos(radians)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, center):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=center)

    def update(self, dt):
        pass


class Tank(pygame.sprite.Sprite):
    def __init__(self, name, color, center, controls):
        super().__init__()
        self.name = name
        self.color = color
        self.controls = controls
        self.original_image = TANK_IMAGES[color]
        self.image = self.original_image
        self.angle = 0.0
        self.position_x = float(center[0])
        self.position_y = float(center[1])
        self.rect = self.image.get_rect(center=center)
        self.base_speed = 225
        self.health = MAX_HEALTH
        self.shield_until = 0.0
        self.speed_until = 0.0
        self.rapid_until = 0.0
        self.next_shot = 0.0
        self.obstacles = []
        self.other_tank = None

    def set_angle(self, angle):
        angle = float(angle)
        if abs(angle - self.angle) < 0.8:
            return
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(
            center=(round(self.position_x), round(self.position_y))
        )

    def _would_hit_something(self):
        if self.rect.left < 0 or self.rect.right > WIDTH:
            return True
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            return True
        if any(self.rect.colliderect(obstacle) for obstacle in self.obstacles):
            return True
        if self.other_tank is not None and self.rect.colliderect(self.other_tank.rect):
            return True
        return False

    def move(self, move_x, move_y, dt):
        if not move_x and not move_y:
            return

        length = math.hypot(move_x, move_y)
        move_x /= length
        move_y /= length
        speed = self.base_speed * (2 if pygame.time.get_ticks() / 1000 < self.speed_until else 1)

        old_x = self.position_x
        self.position_x += move_x * speed * dt
        self.rect.center = (round(self.position_x), round(self.position_y))
        if self._would_hit_something():
            self.position_x = old_x
            self.rect.center = (round(self.position_x), round(self.position_y))

        old_y = self.position_y
        self.position_y += move_y * speed * dt
        self.rect.center = (round(self.position_x), round(self.position_y))
        if self._would_hit_something():
            self.position_y = old_y
            self.rect.center = (round(self.position_x), round(self.position_y))

    def update(self, dt):
        keys = pygame.key.get_pressed()
        move_x = int(keys[self.controls["right"]]) - int(keys[self.controls["left"]])
        move_y = int(keys[self.controls["down"]]) - int(keys[self.controls["up"]])

        if move_x or move_y:
            self.set_angle(math.degrees(math.atan2(move_x, move_y)))
            self.move(move_x, move_y, dt)

    def forward(self):
        return facing_components(self.angle)

    def muzzle_position(self):
        forward_x, forward_y = self.forward()
        return (
            self.rect.centerx + forward_x * 40,
            self.rect.centery + forward_y * 40,
        )

    def can_shoot(self, now):
        return now >= self.next_shot

    def make_bullet(self, now):
        fire_delay = 0.15 if now < self.rapid_until else 0.67
        self.next_shot = now + fire_delay
        direction_x, direction_y = self.forward()
        return Bullet(self, self.muzzle_position(), direction_x, direction_y)

    def take_hit(self, now):
        if now < self.shield_until:
            self.shield_until = 0.0
            return "shield"
        self.health -= 1
        return "health"


class Barrel(pygame.sprite.Sprite):
    def __init__(self, tank, image):
        super().__init__()
        self.tank = tank
        self.original_image = image
        self.image = self.original_image
        self.angle = tank.angle
        self.rect = self.image.get_rect(center=tank.rect.center)

    def update(self, dt):
        if self.angle != self.tank.angle:
            self.angle = self.tank.angle
            self.image = pygame.transform.rotate(self.original_image, self.angle)

        offset_x, offset_y = facing_components(self.angle)
        center = (
            self.tank.rect.centerx + offset_x * 11,
            self.tank.rect.centery + offset_y * 11,
        )
        self.rect = self.image.get_rect(center=center)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, owner, muzzle, direction_x, direction_y):
        super().__init__()
        self.owner = owner
        self.image = BULLET_IMAGES[owner.color]
        self.position_x = float(muzzle[0])
        self.position_y = float(muzzle[1])
        self.speed = 590
        self.velocity_x = direction_x * self.speed
        self.velocity_y = direction_y * self.speed
        self.rect = self.image.get_rect(center=muzzle)

    def update(self, dt):
        self.position_x += self.velocity_x * dt
        self.position_y += self.velocity_y * dt
        self.rect.center = (round(self.position_x), round(self.position_y))
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).colliderect(self.rect):
            self.kill()


class Pickup(pygame.sprite.Sprite):
    INFO = {
        "shield": ("S", CYAN),
        "speed": ("2", GOLD),
        "rapid": ("R", PURPLE),
    }

    def __init__(self, kind, center):
        super().__init__()
        self.kind = kind
        self.image = pygame.Surface((38, 38), pygame.SRCALPHA)
        label, color = self.INFO[kind]
        pygame.draw.circle(self.image, (12, 18, 26, 220), (19, 19), 18)
        pygame.draw.circle(self.image, color, (19, 19), 16, 3)
        draw_text(self.image, label, FONT_MEDIUM, color, (19, 19))
        self.rect = self.image.get_rect(center=center)

    def update(self, dt):
        pass


class Match:
    def __init__(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.tanks = pygame.sprite.Group()
        self.p1_group = pygame.sprite.Group()
        self.p2_group = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.winner = None
        self.message = ""
        self.pickup_time = pygame.time.get_ticks() / 1000 + 6

        self._make_obstacles()

        p1_controls = {
            "left": pygame.K_a, "right": pygame.K_d,
            "up": pygame.K_w, "down": pygame.K_s,
        }
        p2_controls = {
            "left": pygame.K_LEFT, "right": pygame.K_RIGHT,
            "up": pygame.K_UP, "down": pygame.K_DOWN,
        }
        start_y = HEIGHT // 2
        self.player1 = Tank("PLAYER 1", "red", (100, start_y), p1_controls)
        self.player2 = Tank("PLAYER 2", "blue", (WIDTH - 100, start_y), p2_controls)
        self.player1.obstacles = [obstacle.rect for obstacle in self.obstacles]
        self.player2.obstacles = [obstacle.rect for obstacle in self.obstacles]
        self.player1.other_tank = self.player2
        self.player2.other_tank = self.player1

        for tank in (self.player1, self.player2):
            self.tanks.add(tank)
            self.all_sprites.add(tank, layer=2)

        self.p1_group.add(self.player1)
        self.p2_group.add(self.player2)

        self.barrel1 = Barrel(self.player1, BARREL_IMAGES["red"])
        self.barrel2 = Barrel(self.player2, BARREL_IMAGES["blue"])
        self.all_sprites.add(self.barrel1, layer=3)
        self.all_sprites.add(self.barrel2, layer=3)

    def _make_obstacles(self):
        specs = [
            ("tree", (390, 205)),
            ("tree", (810, 495)),
            ("bag", (510, 350)),
            ("bag", (690, 350)),
            ("barrel", (600, 190)),
            ("barrel", (600, 510)),
            ("crate", (300, 455)),
            ("crate", (900, 245)),
        ]
        for kind, center in specs:
            obstacle = Obstacle(OBSTACLE_IMAGES[kind], center)
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle, layer=0)

    def _try_spawn_pickup(self, now):
        if self.pickups or now < self.pickup_time:
            return

        kinds = ("shield", "speed", "rapid")
        for _ in range(50):
            center = (
                random.randint(100, WIDTH - 100),
                random.randint(95, HEIGHT - 80),
            )
            rect = pygame.Rect(0, 0, 42, 42)
            rect.center = center
            if any(rect.colliderect(obstacle.rect.inflate(24, 24)) for obstacle in self.obstacles):
                continue
            if any(rect.colliderect(tank.rect.inflate(75, 75)) for tank in self.tanks):
                continue
            pickup = Pickup(random.choice(kinds), center)
            self.pickups.add(pickup)
            self.all_sprites.add(pickup, layer=1)
            self.pickup_time = now + random.uniform(9, 14)
            return
        self.pickup_time = now + 2

    def _collect_pickups(self, now):
        for pickup in list(self.pickups):
            for tank in self.tanks:
                if not pickup.rect.colliderect(tank.rect):
                    continue
                if pickup.kind == "shield":
                    tank.shield_until = now + POWERUP_DURATION
                elif pickup.kind == "speed":
                    tank.speed_until = now + POWERUP_DURATION
                elif pickup.kind == "rapid":
                    tank.rapid_until = now + POWERUP_DURATION
                pickup.kill()
                break

    def _fire(self, now):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.player1.can_shoot(now):
            bullet = self.player1.make_bullet(now)
            self.bullets.add(bullet)
            self.all_sprites.add(bullet, layer=4)

        if keys[pygame.K_RETURN] and self.player2.can_shoot(now):
            bullet = self.player2.make_bullet(now)
            self.bullets.add(bullet)
            self.all_sprites.add(bullet, layer=4)

    def _resolve_bullets(self, now):
        for bullet in list(self.bullets):
            if any(bullet.rect.colliderect(obstacle.rect) for obstacle in self.obstacles):
                bullet.kill()
                continue

            targets = self.p2_group if bullet.owner is self.player1 else self.p1_group
            hit_target = next(
                (tank for tank in targets if bullet.rect.colliderect(tank.rect)),
                None,
            )
            if hit_target is None:
                continue

            bullet.kill()
            result = hit_target.take_hit(now)
            if result == "health" and hit_target.health <= 0:
                self.winner = bullet.owner.name
                self.message = f"{hit_target.name} was knocked out!"
                hit_target.kill()

    def update(self, dt, now):
        if self.winner is not None:
            return
        self._fire(now)
        self.all_sprites.update(dt)
        self._collect_pickups(now)
        self._resolve_bullets(now)
        self._try_spawn_pickup(now)

    def draw_background(self, surface):
        for y in range(0, HEIGHT, GRASS.get_height()):
            for x in range(0, WIDTH, GRASS.get_width()):
                surface.blit(GRASS, (x, y))
        pygame.draw.rect(surface, (20, 38, 45), (0, 0, WIDTH, HEIGHT), 8)

    def draw_hud(self, surface, now):
        for tank in self.tanks:
            x, y = tank.rect.centerx, tank.rect.top - 11
            bar_width = 58
            bar = pygame.Rect(x - bar_width // 2, y - 5, bar_width, 8)
            pygame.draw.rect(surface, (25, 30, 35), bar, border_radius=4)
            fill_width = int(bar_width * max(0, tank.health) / MAX_HEALTH)
            if fill_width:
                fill = pygame.Rect(bar.left, bar.top, fill_width, bar.height)
                health_color = GREEN if tank.health > 1 else GOLD
                pygame.draw.rect(surface, health_color, fill, border_radius=4)
            if now < tank.shield_until:
                pygame.draw.circle(surface, CYAN, tank.rect.center, 39, 2)

        panel = pygame.Rect(16, 14, WIDTH - 32, 48)
        pygame.draw.rect(surface, (8, 18, 28, 210), panel, border_radius=10)
        label = f"{self.player1.name}: {max(0, self.player1.health)}/{MAX_HEALTH}"
        other = f"PLAYER 2: {max(0, self.player2.health)}/{MAX_HEALTH}"
        draw_text(surface, label, FONT_SMALL, RED, (130, 38))
        draw_text(surface, "ESC  MENU     F11  FULLSCREEN", FONT_SMALL, WHITE, (WIDTH // 2, 38))
        draw_text(surface, other, FONT_SMALL, BLUE, (WIDTH - 132, 38))

        effect_text = []
        if now < self.player1.shield_until:
            effect_text.append("P1 SHIELD")
        if now < self.player1.speed_until:
            effect_text.append("P1 SPEED")
        if now < self.player1.rapid_until:
            effect_text.append("P1 RAPID")
        if now < self.player2.shield_until:
            effect_text.append("P2 SHIELD")
        if now < self.player2.speed_until:
            effect_text.append("P2 SPEED")
        if now < self.player2.rapid_until:
            effect_text.append("P2 RAPID")
        if effect_text:
            draw_text(surface, "  |  ".join(effect_text), FONT_SMALL, CYAN, (WIDTH // 2, HEIGHT - 20))

        controls = "P1 WASD + SPACE     P2 ARROWS + ENTER"
        draw_text(surface, controls, FONT_SMALL, (230, 238, 225), (WIDTH // 2, HEIGHT - 48))

    def draw(self, surface, now):
        self.draw_background(surface)
        self.all_sprites.draw(surface)
        self.draw_hud(surface, now)
        if self.winner is not None:
            draw_overlay(surface)
            draw_text(surface, f"{self.winner} WINS!", FONT_LARGE, GOLD, (WIDTH // 2, HEIGHT // 2 - 26))
            draw_text(surface, self.message, FONT_MEDIUM, WHITE, (WIDTH // 2, HEIGHT // 2 + 24))
            draw_text(surface, "R  REMATCH       M  MAIN MENU", FONT_SMALL, CYAN, (WIDTH // 2, HEIGHT // 2 + 72))


def draw_overlay(surface):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((4, 11, 18, 168))
    surface.blit(overlay, (0, 0))


def make_match():
    return Match()


def draw_menu(surface):
    surface.fill((30, 34, 38))

    draw_text(surface, "TANK SHOOTERS", FONT_LARGE, WHITE, (WIDTH // 2, 145))

    start_button = pygame.Rect(WIDTH // 2 - 220, 255, 440, 60)
    draw_text(surface, "1 - Start Two Player Game", FONT_MEDIUM, WHITE, start_button.center)

    draw_text(surface, "Player 1: WASD to move, SPACE to fire", FONT_SMALL, WHITE, (WIDTH // 2, 445))
    draw_text(surface, "Player 2: ARROWS to move, ENTER to fire", FONT_SMALL, WHITE, (WIDTH // 2, 475))
    draw_text(surface, "Pickups: shield, double speed, rapid fire", FONT_SMALL, WHITE, (WIDTH // 2, 525))
    draw_text(surface, "F11: fullscreen", FONT_SMALL, WHITE, (WIDTH // 2, 585))
    return start_button


pygame.mixer.music.load("assets/Music/theme.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

def main():
    global screen
    state = "menu"
    match = None
    running = True

    while running:
        dt = min(clock.tick(FPS) / 1000, 0.04)
        now = pygame.time.get_ticks() / 1000
        start_button = None
        if state == "menu":
            start_button = draw_menu(screen)
        elif state == "playing":
            match.update(dt, now)
            if match.winner is not None:
                state = "game_over"
            match.draw(screen, now)
        elif state == "game_over" and match is not None:
            match.draw(screen, now)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    if screen.get_flags() & pygame.FULLSCREEN:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    else:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

                elif state == "menu":
                    if event.key == pygame.K_1:
                        match = make_match()
                        state = "playing"

                elif state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        state = "menu"

                elif state == "game_over":
                    if event.key == pygame.K_r:
                        match = make_match()
                        state = "playing"
                    elif event.key in (pygame.K_m, pygame.K_ESCAPE):
                        state = "menu"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and state == "menu":
                if start_button.collidepoint(event.pos):
                    match = make_match()
                    state = "playing"

    pygame.quit()


if __name__ == "__main__":
    main()

