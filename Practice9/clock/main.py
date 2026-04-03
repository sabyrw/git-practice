import pygame
import datetime

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")
clock = pygame.time.Clock()

# Суреттерді жүктеу
body_img = pygame.image.load('body.jpeg').convert_alpha()
hand_min_raw = pygame.image.load('second_hand.png').convert_alpha()
hand_sec_raw = pygame.image.load('minut_hand.png').convert_alpha()

# --- ӨЗГЕРТІЛГЕН БӨЛІМ (Жуандығы реттелген) ---
hand_min_img = pygame.transform.scale(hand_min_raw, (140, 320)) # Ені 40-тан 100-ге өзгерді
hand_sec_img = pygame.transform.scale(hand_sec_raw, (120, 320))  # Ені 25-тен 80-ге өзгерді

def blit_rotate_pivot(surf, image, pos, originPos, angle):
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, -angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)

# Сағаттың ортасы
center = (WIDTH // 2, HEIGHT // 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    second = now.second
    minute = now.minute
    
    smooth_minute = minute * 6 + (second * 0.1)
    smooth_second = second * 6

    screen.fill((255, 255, 255))
    
    screen.blit(body_img, body_img.get_rect(center=center))

    # Тілдердің орталық нүктесі (pivot)
    min_pivot = (hand_min_img.get_width() // 2, hand_min_img.get_height() - 120)
    blit_rotate_pivot(screen, hand_min_img, center, min_pivot, smooth_minute)

    sec_pivot = (hand_sec_img.get_width() // 2, hand_sec_img.get_height() - 110)
    blit_rotate_pivot(screen, hand_sec_img, center, sec_pivot, smooth_second)

    pygame.draw.circle(screen, (0, 0, 0), center, 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()