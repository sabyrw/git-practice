import pygame
import sys
import math
import os
from datetime import datetime
from tools import flood_fill

def main():
    pygame.init()
    
    # Экран параметрлері
    W, H = 800, 600
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("KBTU Paint Pro 2026")
    
    # Канвас (сурет салынатын қабат)
    canvas = pygame.Surface((W, H))
    canvas.fill((0, 0, 0))
    
    clock = pygame.time.Clock()
    
    # Папканы тексеру
    if not os.path.exists('assets'):
        os.makedirs('assets')

    # --- SETTINGS ---
    mode = "brush"      # brush, line, rect, circle, fill, text, eraser
    color = (255, 0, 0) # Бастапқы түс - Қызыл
    thickness = 2       # 2, 5, 10
    
    drawing = False
    start_pos = None
    
    # Text Tool айнымалылары
    font = pygame.font.SysFont("Arial", 24)
    text_input = ""
    text_pos = None
    text_active = False

    while True:
        # Экранды жаңарту
        screen.blit(canvas, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 1. Клавиатура батырмалары
            if event.type == pygame.KEYDOWN:
                # Ctrl + S арқылы сақтау
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    fname = f"assets/paint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    pygame.image.save(canvas, fname)
                    print(f"Сақталды: {fname}")

                # Мәтін теру режимі
                if text_active:
                    if event.key == pygame.K_RETURN:
                        txt_img = font.render(text_input, True, color)
                        canvas.blit(txt_img, text_pos)
                        text_active = False
                        text_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        text_active = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode
                    continue # Мәтін жазып жатқанда басқа батырмалар істемейді

                # Құралдар (1-7)
                if event.key == pygame.K_1: mode = "brush"
                elif event.key == pygame.K_2: mode = "line"
                elif event.key == pygame.K_3: mode = "rect"
                elif event.key == pygame.K_4: mode = "circle"
                elif event.key == pygame.K_5: mode = "fill"
                elif event.key == pygame.K_6: mode = "text"
                elif event.key == pygame.K_7: mode = "eraser"

                # Қалыңдық (F1, F2, F3)
                if event.key == pygame.K_F1: thickness = 2
                elif event.key == pygame.K_F2: thickness = 5
                elif event.key == pygame.K_F3: thickness = 10

                # Түстер (R, G, B)
                if event.key == pygame.K_r: color = (255, 0, 0)
                elif event.key == pygame.K_g: color = (0, 255, 0)
                elif event.key == pygame.K_b: color = (0, 0, 255)
                elif event.key == pygame.K_w: color = (255, 255, 255)

            # 2. Тышқан батырмалары
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode == "fill":
                    flood_fill(canvas, event.pos[0], event.pos[1], color)
                elif mode == "text":
                    text_active = True
                    text_pos = event.pos
                    text_input = ""
                else:
                    drawing = True
                    start_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing and start_pos:
                    x1, y1 = start_pos
                    x2, y2 = event.pos
                    
                    if mode == "line":
                        pygame.draw.line(canvas, color, start_pos, event.pos, thickness)
                    elif mode == "rect":
                        pygame.draw.rect(canvas, color, (min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1)), thickness)
                    elif mode == "circle":
                        r = int(math.hypot(x2-x1, y2-y1))
                        pygame.draw.circle(canvas, color, (x1, y1), r, thickness)
                    
                    drawing = False
                    start_pos = None

            if event.type == pygame.MOUSEMOTION and drawing:
                if mode == "brush":
                    pygame.draw.circle(canvas, color, event.pos, thickness)
                elif mode == "eraser":
                    pygame.draw.circle(canvas, (0,0,0), event.pos, thickness * 5)

        # --- PREVIEWS (Алдын-ала көрсету) ---
        if drawing and start_pos:
            curr_pos = pygame.mouse.get_pos()
            if mode == "line":
                pygame.draw.line(screen, color, start_pos, curr_pos, thickness)
            elif mode == "rect":
                x1, y1 = start_pos
                x2, y2 = curr_pos
                pygame.draw.rect(screen, color, (min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1)), thickness)
            elif mode == "circle":
                r = int(math.hypot(curr_pos[0]-start_pos[0], curr_pos[1]-start_pos[1]))
                pygame.draw.circle(screen, color, start_pos, r, thickness)

        # Мәтін жазып жатқандағы көрініс
        if text_active:
            txt_surf = font.render(text_input + "|", True, color)
            screen.blit(txt_surf, text_pos)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()