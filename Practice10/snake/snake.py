import pygame
import sys
import random

pygame.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 600, 600
CELL = 20   # grid өлшемі

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
WHITE = (255,255,255)
GREEN = (0,200,0)
RED = (200,0,0)
BLACK = (0,0,0)

# ---------------- SNAKE ----------------
snake = [(100,100), (80,100), (60,100)]  # бастапқы дене
direction = (20,0)  # оңға қозғалады

# -------------- Game Over ----------------

def game_over():
    screen.fill((200,0,0))  # қызыл фон

    font_big = pygame.font.SysFont("Arial", 50)
    font_small = pygame.font.SysFont("Arial", 30)

    text1 = font_big.render("GAME OVER", True, (255,255,255))
    text2 = font_small.render(f"Score: {score}", True, (255,255,255))
    text3 = font_small.render(f"Level: {level}", True, (255,255,255))

    screen.blit(text1, (150, 200))
    screen.blit(text2, (220, 280))
    screen.blit(text3, (220, 320))

    pygame.display.update()
    pygame.time.delay(3000)  # 3 секунд көрсетеді

    pygame.quit()
    sys.exit()

# ---------------- FOOD ----------------
def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        # snake үстіне түспеу
        if (x,y) not in snake:
            return (x,y)

food = generate_food()

# ---------------- SCORE & LEVEL ----------------
score = 0
level = 1
speed = 8

font = pygame.font.SysFont("Arial", 25)

# ---------------- GAME LOOP ----------------
while True:

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # басқару
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0,20):
                direction = (0,-20)
            if event.key == pygame.K_DOWN and direction != (0,-20):
                direction = (0,20)
            if event.key == pygame.K_LEFT and direction != (20,0):
                direction = (-20,0)
            if event.key == pygame.K_RIGHT and direction != (-20,0):
                direction = (20,0)

    # -------- MOVE SNAKE --------
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)

    # -------- WALL COLLISION --------
    if (head[0] < 0 or head[0] >= WIDTH or 
        head[1] < 0 or head[1] >= HEIGHT):
            game_over()
        

    # -------- SELF COLLISION --------
    if head in snake[1:]:
        game_over()

    # -------- EAT FOOD --------
    if head == food:
        score += 1
        food = generate_food()
    else:
        snake.pop()  # құйрықты қысқарту

    # -------- LEVEL SYSTEM --------
    if score >= level * 4:   # әр 4 food сайын level ↑
        level += 1
        speed += 2

    # -------- DRAW --------
    screen.fill(WHITE)

    # snake салу
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL, CELL))

    # food салу
    pygame.draw.rect(screen, RED, (*food, CELL, CELL))

    # score + level
    text = font.render(f"Score: {score}  Level: {level}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(speed)