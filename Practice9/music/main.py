import pygame
import sys
import os
from player import MusicPlayer

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 600, 300  # taller for controls
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Keyboard Music Player")
font = pygame.font.SysFont('Arial', 28)
small_font = pygame.font.SysFont('Arial', 22)
clock = pygame.time.Clock()

# Get path to 'music' folder relative to this script
current_dir = os.path.dirname(os.path.abspath(__file__))
music_folder = os.path.join(current_dir, "music")

# Initialize Music Player
try:
    player = MusicPlayer(music_folder)
except FileNotFoundError as e:
    print(e)
    sys.exit(1)

player.play()  # auto-start first track

running = True
while running:
    screen.fill((30, 30, 30))  # dark background

    # Display current track and position
    track_text = font.render(f"Track: {player.get_current_track()}", True, (255, 255, 255))
    pos_text = font.render(f"Position: {player.get_position()}s", True, (255, 255, 0))
    screen.blit(track_text, (20, 50))
    screen.blit(pos_text, (20, 100))

    # Display keyboard controls
    controls = [
        "P = Play",
        "S = Stop",
        "N = Next track",
        "B = Previous (Back)",
        "Q = Quit"
    ]
    for i, ctrl in enumerate(controls):
        ctrl_text = small_font.render(ctrl, True, (200, 200, 200))
        screen.blit(ctrl_text, (20, 150 + i*30))  # vertical spacing

    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.previous_track()
            elif event.key == pygame.K_q:
                running = False

    clock.tick(30)

pygame.quit()
sys.exit()