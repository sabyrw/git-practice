import pygame
import sys
import math

def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint App FULL FIX")

    clock = pygame.time.Clock()

    canvas = pygame.Surface((640, 480))
    canvas.fill((0, 0, 0))

    # ---------------- SETTINGS ----------------
    mode = "brush"
    color_mode = "red"
    radius = 5

    drawing = False
    start_pos = None

    # 🎨 түс таңдау
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

            # ❌ шығу
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ⌨️ клавиатура
            if event.type == pygame.KEYDOWN:

                # құралдар
                if event.key == pygame.K_1:
                    mode = "brush"
                elif event.key == pygame.K_2:
                    mode = "rect"
                elif event.key == pygame.K_3:
                    mode = "circle"
                elif event.key == pygame.K_4:
                    mode = "eraser"
                elif event.key == pygame.K_5:
                    mode = "square"
                elif event.key == pygame.K_6:
                    mode = "right_triangle"
                elif event.key == pygame.K_7:
                    mode = "equilateral_triangle"
                elif event.key == pygame.K_8:
                    mode = "rhombus"

                # түстер
                elif event.key == pygame.K_r:
                    color_mode = "red"
                elif event.key == pygame.K_g:
                    color_mode = "green"
                elif event.key == pygame.K_b:
                    color_mode = "blue"

            # 🖱 басу
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos

            # 🖱 жіберу → фигура салынады
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False

                if not start_pos:
                    continue

                x1, y1 = start_pos
                x2, y2 = event.pos

                color = get_color()

                # ⬛ RECT
                if mode == "rect":
                    pygame.draw.rect(canvas, color,
                                     (min(x1,x2), min(y1,y2),
                                      abs(x2-x1), abs(y2-y1)), 2)

                # ⭕ CIRCLE
                elif mode == "circle":
                    r = int(math.hypot(x2 - x1, y2 - y1))
                    pygame.draw.circle(canvas, color, (x1, y1), r, 2)

                # ⬜ SQUARE (толық fix)
                elif mode == "square":
                    size = min(abs(x2-x1), abs(y2-y1))
                    x = x1 if x2 > x1 else x1 - size
                    y = y1 if y2 > y1 else y1 - size

                    pygame.draw.rect(canvas, color, (x, y, size, size), 2)

                # 📐 RIGHT TRIANGLE
                elif mode == "right_triangle":
                    points = [
                        (x1, y1),
                        (x2, y1),
                        (x1, y2)
                    ]
                    pygame.draw.polygon(canvas, color, points, 2)

                # 🔺 EQUILATERAL TRIANGLE
                elif mode == "equilateral_triangle":
                    side = abs(x2 - x1)
                    height = int(side * math.sqrt(3) / 2)

                    # бағыт fix
                    if y2 > y1:
                        height = -height

                    points = [
                        (x1, y1),
                        (x1 + side, y1),
                        (x1 + side // 2, y1 - height)
                    ]
                    pygame.draw.polygon(canvas, color, points, 2)

                # 🔷 RHOMBUS
                elif mode == "rhombus":
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    dx = abs(x2 - x1) // 2
                    dy = abs(y2 - y1) // 2

                    points = [
                        (cx, cy - dy),
                        (cx + dx, cy),
                        (cx, cy + dy),
                        (cx - dx, cy)
                    ]
                    pygame.draw.polygon(canvas, color, points, 2)

                start_pos = None

            # ✏️ brush / eraser
            if event.type == pygame.MOUSEMOTION and drawing:
                if mode == "brush":
                    pygame.draw.circle(canvas, get_color(), event.pos, radius)

                elif mode == "eraser":
                    pygame.draw.circle(canvas, (0,0,0), event.pos, radius*2)

        # 🖥 көрсету
        screen.blit(canvas, (0, 0))
        pygame.display.update()
        clock.tick(60)

main()