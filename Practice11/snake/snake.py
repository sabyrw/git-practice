import pygame
import sys
import random

pygame.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 600, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
WHITE = (255,255,255)
GREEN = (0,200,0)
RED = (200,0,0)
BLACK = (0,0,0)
YELLOW = (255,255,0)

# ---------------- SNAKE ----------------
snake = [(100,100), (80,100), (60,100)]
direction = (20,0)

# ---------------- GAME OVER ----------------
def game_over():
    screen.fill((200,0,0))

    font_big = pygame.font.SysFont("Arial", 50)
    font_small = pygame.font.SysFont("Arial", 30)

    text1 = font_big.render("GAME OVER", True, (255,255,255))
    text2 = font_small.render(f"Score: {score}", True, (255,255,255))
    text3 = font_small.render(f"Level: {level}", True, (255,255,255))

    screen.blit(text1, (150, 200))
    screen.blit(text2, (220, 280))
    screen.blit(text3, (220, 320))

    pygame.display.update()
    pygame.time.delay(3000)

    pygame.quit()
    sys.exit()

# ---------------- NORMAL FOOD ----------------
def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        if (x,y) not in snake:
            return (x,y)

food = generate_food()

# ---------------- BONUS FOOD ----------------
class BonusFood:
    def __init__(self):
        self.position = generate_food()
        self.size = CELL * 2  # ⭐ үлкен
        self.timer = random.randint(120, 180)  # 2–3 сек (60 FPS)
        self.active = True

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.active = False  # ⏱ жоғалады

    def draw(self):
        pygame.draw.rect(screen, YELLOW,
                         (self.position[0], self.position[1],
                          self.size, self.size))

bonus_food = None  # басында жоқ

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

    # -------- COLLISIONS --------
    if (head[0] < 0 or head[0] >= WIDTH or 
        head[1] < 0 or head[1] >= HEIGHT):
        game_over()

    if head in snake[1:]:
        game_over()

    # -------- NORMAL FOOD --------
    if head == food:
        score += 1
        food = generate_food()
    else:
        snake.pop()

    # -------- BONUS FOOD SPAWN --------
    if bonus_food is None and random.randint(1, 200) == 1:
        bonus_food = BonusFood()

    # -------- BONUS FOOD UPDATE --------
    if bonus_food:
        bonus_food.update()

        # Егер snake жесе
        bx, by = bonus_food.position
        if (bx <= head[0] < bx + bonus_food.size and
            by <= head[1] < by + bonus_food.size):
            score += 3  # ⭐ көп ұпай
            bonus_food = None

        # Егер уақыты бітсе
        elif not bonus_food.active:
            bonus_food = None

    # -------- LEVEL --------
    if score >= level * 4:
        level += 1
        speed += 2

    # -------- DRAW --------
    screen.fill(WHITE)

    # snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL, CELL))

    # normal food
    pygame.draw.rect(screen, RED, (*food, CELL, CELL))

    # bonus food
    if bonus_food:
        bonus_food.draw()

        # ⏱ секундпен таймер
        seconds = bonus_food.timer // 60
        timer_text = font.render(f"Bonus: {seconds}s", True, BLACK)
        screen.blit(timer_text, (400, 10))

    # UI
    text = font.render(f"Score: {score}  Level: {level}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(speed)