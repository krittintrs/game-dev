import pygame, random

from constant import *

class Ball:
    def __init__(self, screen, x, y, width, height) -> None:
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)

        self.dx = random.choice([-300, 300])   # randomly choose between go left or right
        self.dy = random.randint(-150, 150)    # randomly select y speed
    
    def Reset(self):
        self.rect.x = WIDTH/2 - 6
        self.rect.y = HEIGHT/2 - 6
        self.dx = random.choice([-300, 300])
        self.dy = random.randint(-150, 150)

    def update(self, dt):
        self.rect.x += self.dx * dt
        self.rect.y += self.dy * dt

    def render(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)
        