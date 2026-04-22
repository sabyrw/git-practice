import pygame, sys
from pygame.locals import *
import random

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# ---------------- COLORS ----------------
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY  = (50, 50, 50)
YELLOW = (255,255,0)

# ---------------- SCREEN ----------------
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((400,600))
pygame.display.set_caption("Racer")

# ---------------- ENEMY ----------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

        self.speed = 7  # 🚗 бастапқы speed

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

    def increase_speed(self):
        self.speed += 1  # 🚀 speed өсіру

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ---------------- PLAYER ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ---------------- COIN ----------------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.rect = pygame.Rect(0, 0, 30, 30)

        self.rect.x = random.randint(20, SCREEN_WIDTH-40)
        self.rect.y = -50
        self.speed = 5

        # 🪙 weight (ұпай)
        self.weight = random.choice([1, 2, 3])

        # 🎨 түсі weight-ке байланысты
        if self.weight == 1:
            self.color = YELLOW
        elif self.weight == 2:
            self.color = GREEN
        else:
            self.color = RED

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, 15)


# ---------------- OBJECTS ----------------
P1 = Player()
E1 = Enemy()
coins = []

score = 0
coins_collected = 0  # қанша coin жиналды

font = pygame.font.SysFont("Arial", 25)

# -------- ROAD ANIMATION --------
road_y = 0

# ⚡ LEVEL UP эффект таймері
speed_message_timer = 0

# ---------------- GAME LOOP ----------------
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # -------- UPDATE --------
    P1.update()
    E1.move()

    # -------- GAME OVER --------
    if P1.rect.colliderect(E1.rect):
        DISPLAYSURF.fill(RED)

        font_big = pygame.font.SysFont("Arial", 50)
        game_over_text = font_big.render("GAME OVER", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)

        DISPLAYSURF.blit(game_over_text, (60, 250))
        DISPLAYSURF.blit(score_text, (130, 320))

        pygame.display.update()
        pygame.time.delay(4000)

        pygame.quit()
        sys.exit()

    # -------- COIN SPAWN --------
    if random.randint(1, 40) == 1:
        coins.append(Coin())

    # -------- ROAD DRAW --------
    DISPLAYSURF.fill(GRAY)

    pygame.draw.rect(DISPLAYSURF, YELLOW, (0, 0, 10, SCREEN_HEIGHT))
    pygame.draw.rect(DISPLAYSURF, YELLOW, (390, 0, 10, SCREEN_HEIGHT))

    road_y += 5
    if road_y >= 40:
        road_y = 0

    for y in range(-40, SCREEN_HEIGHT, 40):
        pygame.draw.rect(DISPLAYSURF, WHITE, (190, y + road_y, 20, 20))

    # -------- DRAW OBJECTS --------
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)

    # -------- COINS --------
    for coin in coins[:]:
        coin.move()
        coin.draw(DISPLAYSURF)

        if coin.rect.top > SCREEN_HEIGHT:
            coins.remove(coin)

        if P1.rect.colliderect(coin.rect):
            coins.remove(coin)

            score += coin.weight
            coins_collected += 1

            # 🚗 әр 5 coin сайын speed өседі
            if coins_collected % 5 == 0:
                E1.increase_speed()
                speed_message_timer = 60  # ⚡ эффект

    # -------- TEXT --------
    score_text = font.render(f"Score: {score}", True, BLACK)
    speed_text = font.render(f"Speed: {E1.speed}", True, BLACK)

    DISPLAYSURF.blit(score_text, (SCREEN_WIDTH - 150, 10))
    DISPLAYSURF.blit(speed_text, (10, 10))

    # ⚡ LEVEL UP эффект
    if speed_message_timer > 0:
        font_big = pygame.font.SysFont("Arial", 40)
        msg = font_big.render("LEVEL UP!", True, RED)
        DISPLAYSURF.blit(msg, (100, 250))
        speed_message_timer -= 1

    pygame.display.update()
    FramePerSec.tick(FPS)