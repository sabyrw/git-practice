import pygame

def flood_fill(surface, x, y, new_color):
    """BFS алгоритмі арқылы тұйықталған аймақты бояу"""
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    
    width, height = surface.get_size()
    queue = [(x, y)]
    
    while queue:
        curr_x, curr_y = queue.pop(0)
        if surface.get_at((curr_x, curr_y)) != target_color:
            continue
            
        surface.set_at((curr_x, curr_y), new_color)
        
        # Көршілес пиксельдер (оң, сол, жоғары, төмен)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = curr_x + dx, curr_y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if surface.get_at((nx, ny)) == target_color:
                    queue.append((nx, ny))