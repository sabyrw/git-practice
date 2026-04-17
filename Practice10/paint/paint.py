import pygame
import sys
import math

def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint App - Tools + Colors")

    clock = pygame.time.Clock()

    canvas = pygame.Surface((640, 480))
    canvas.fill((0, 0, 0))

    # SETTINGS
    mode = "brush"
    color_mode = "red"
    radius = 5

    drawing = False
    start_pos = None

    def get_color():
        if color_mode == "red":
            return (255, 0, 0)
        elif color_mode == "green":
            return (0, 255, 0)
        elif color_mode == "blue":
            return (0, 0, 255)
        return (255, 255, 255)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # KEYBOARD CONTROLS
            if event.type == pygame.KEYDOWN:

                # TOOLS
                if event.key == pygame.K_1:
                    mode = "brush"
                elif event.key == pygame.K_2:
                    mode = "rect"
                elif event.key == pygame.K_3:
                    mode = "circle"
                elif event.key == pygame.K_4:
                    mode = "eraser"

                # COLORS
                elif event.key == pygame.K_r:
                    color_mode = "red"
                elif event.key == pygame.K_g:
                    color_mode = "green"
                elif event.key == pygame.K_b:
                    color_mode = "blue"

            # MOUSE DOWN
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos

            # MOUSE UP
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False

                # RECTANGLE
                if mode == "rect" and start_pos:
                    x1, y1 = start_pos
                    x2, y2 = event.pos
                    pygame.draw.rect(
                        canvas,
                        get_color(),
                        (x1, y1, x2 - x1, y2 - y1),
                        2
                    )

                # CIRCLE
                elif mode == "circle" and start_pos:
                    x1, y1 = start_pos
                    x2, y2 = event.pos
                    r = int(math.hypot(x2 - x1, y2 - y1))
                    pygame.draw.circle(
                        canvas,
                        get_color(),
                        (x1, y1),
                        r,
                        2
                    )

            # DRAW BRUSH / ERASER
            if event.type == pygame.MOUSEMOTION and drawing:
                pos = event.pos

                if mode == "brush":
                    pygame.draw.circle(canvas, get_color(), pos, radius)

                elif mode == "eraser":
                    pygame.draw.circle(canvas, (0, 0, 0), pos, radius * 2)

        # RENDER
        screen.blit(canvas, (0, 0))
        pygame.display.update()
        clock.tick(60)

main()