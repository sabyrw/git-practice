import pygame

class Ball:
    def __init__(self, x, y, radius, color, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 20  # әр басылған пернемен қозғалыс

    def move(self, dx, dy):
        """Шарды қозғалысқа келтіру, экраннан шықпауын тексеру"""
        new_x = self.x + dx
        new_y = self.y + dy

        # Шекараларды тексеру
        if self.radius <= new_x <= self.screen_width - self.radius:
            self.x = new_x
        if self.radius <= new_y <= self.screen_height - self.radius:
            self.y = new_y

    def draw(self, screen):
        """Шарды экранға салу"""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)