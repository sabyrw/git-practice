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

    def move(self):
        # төмен қозғалу
        self.rect.move_ip(0,7)

        # экраннан шықса қайтадан жоғарыдан шығады
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

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

        # солға қозғалу
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        # оңға қозғалу
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)     


# ---------------- COIN ----------------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(20, SCREEN_WIDTH-40)
        self.rect.y = -50
        self.speed = 5

    def move(self):
        self.rect.y += self.speed   # 👈 МІНДЕТТІ

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ---------------- OBJECTS ----------------
P1 = Player()
E1 = Enemy()
coins = []   # coin тізімі
score = 0    # жинаған coin саны

# текст үшін
font = pygame.font.SysFont("Arial", 25)

# ---------------- GAME LOOP ----------------
while True:

    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # -------- UPDATE --------
    P1.update()
    E1.move()

        # -------- GAME OVER CHECK --------
    if P1.rect.colliderect(E1.rect):
        # экранды қара қыламыз
        DISPLAYSURF.fill(RED)

        # текст шығару
        font_big = pygame.font.SysFont("Arial", 50)
        game_over_text = font_big.render("GAME OVER", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)

        DISPLAYSURF.blit(game_over_text, (60, 250))
        DISPLAYSURF.blit(score_text, (130, 320))

        pygame.display.update()

        # 2 секунд күту
        pygame.time.delay(4000)

        pygame.quit()
        sys.exit()


    # coin random
    if random.randint(1, 40) == 1:
        coins.append(Coin())

    # -------- DRAW --------
    DISPLAYSURF.fill(WHITE)

    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)


    # -------- COINS --------
    for coin in coins[:]:
        coin.move()
        coin.draw(DISPLAYSURF)

        # экраннан шықса өшіреміз
        if coin.rect.top > SCREEN_HEIGHT:
            coins.remove(coin)

        # -------- COLLISION --------
        if P1.rect.colliderect(coin.rect):
            coins.remove(coin)
            score += 1   # coin жинады

    # -------- SCORE --------
    text = font.render(f"Coins: {score}", True, BLACK)
    DISPLAYSURF.blit(text, (SCREEN_WIDTH - 130, 10))

    pygame.display.update()
    FramePerSec.tick(FPS)