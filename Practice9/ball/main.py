import pygame
import sys
from ball import Ball

# Инициализация
pygame.init()

# Терезе өлшемдері
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")

# FPS бақылау
clock = pygame.time.Clock()

# Шарды жасау
ball = Ball(x=WIDTH//2, y=HEIGHT//2, radius=25, color=(255,0,0),
            screen_width=WIDTH, screen_height=HEIGHT)

# Ойын циклі
running = True
while running:
    screen.fill((255, 255, 255))  # ақ фон

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Пернелерді тексеру
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ball.move(-ball.speed, 0)
            elif event.key == pygame.K_RIGHT:
                ball.move(ball.speed, 0)
            elif event.key == pygame.K_UP:
                ball.move(0, -ball.speed)
            elif event.key == pygame.K_DOWN:
                ball.move(0, ball.speed)

    # Шарды экранға салу
    ball.draw(screen)

    pygame.display.flip()
    clock.tick(30)  # 30 FPS

pygame.quit()
sys.exit()