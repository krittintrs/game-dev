import pygame
import math
from constant import *
from Ball import Ball

from enum import Enum

class PaddleSize(Enum):
    TINY = 20
    SMALL = 40
    MEDIUM = 60
    LARGE = 80
    HUGE = 100

class Paddle:
    def __init__(self, screen, x, y, width, size: PaddleSize, color):
        self.screen = screen

        self.rect = pygame.Rect(x, y, width, size.value)
        self.color = color
        self.dy = 0

    def update(self, dt):
        if self.dy > 0:
            if self.rect.y + self.rect.height < HEIGHT:
                self.rect.y += self.dy*dt
        else:
            if self.rect.y >= 0:
                self.rect.y += self.dy*dt

    def render(self):
        # Neon glow effect
        glow_color = self.color
        glow_width = 5
        inner_color = (0, 0, 0)

        # Draw the outer glowing border (neon effect)
        pygame.draw.rect(self.screen, glow_color, self.rect.inflate(glow_width, glow_width), border_radius=5)

        # Draw the inner solid color paddle
        pygame.draw.rect(self.screen, inner_color, self.rect, border_radius=5)

    def Reset(self):
        self.rect.height = PaddleSize.MEDIUM.value

class WeakAIPaddle(Paddle):
    def __init__(self, screen, x, y, width, height, color):
        super().__init__(screen, x, y, width, height, color)

    def update(self, dt, ball: Ball):
        paddle_y = self.rect.centery
        ball_y = ball.rect.centery

        if ball_y > paddle_y:
            self.dy = 200
        elif ball_y == paddle_y:
            self.dy = 0
        else:
            self.dy = -200
            
        
        diff = math.fabs(ball_y - paddle_y)
        if diff > 200:
            self.dy *= 8
        elif diff > 100:
            self.dy *= 4
        elif diff > 50:
            self.dy *= 2
        elif diff < 10:
            self.dy *= 0

        # print(ball.dy, ball_y, '/', paddle_y, diff)

        super().update(dt)

class StrongAIPaddle(Paddle):
    def __init__(self, screen, x, y, width, height, color):
        super().__init__(screen, x, y, width, height, color)

    def update(self, dt, ball: Ball):
        paddle_y = self.rect.centery
        ball_x = ball.rect.centerx
        ball_y = ball.rect.centery

        t = math.fabs((WIDTH - ball_x) / (ball.dx + 0.001))
        expected_y = ball_y + ball.dy * t

        if expected_y > paddle_y:
            self.dy = 200
        elif expected_y == paddle_y:
            self.dy = 0
        else:
            self.dy = -200
            
        
        diff = math.fabs(expected_y - paddle_y)
        if diff > 200:
            self.dy *= 8
        elif diff > 100:
            self.dy *= 4
        elif diff > 50:
            self.dy *= 2
        elif diff < 10:
            self.dy *= 0

        # print(ball.dy, ball_y, '/', paddle_y, diff)
        # print(ball.dy, dt, t, expected_y)

        super().update(dt)

class StrongAIPaddleLeft(Paddle):
    def __init__(self, screen, x, y, width, height, color):
        super().__init__(screen, x, y, width, height, color)

    def update(self, dt, ball: Ball):
        paddle_y = self.rect.centery
        ball_x = ball.rect.centerx
        ball_y = ball.rect.centery

        t = math.fabs((ball_x) / (ball.dx + 0.001))
        expected_y = ball_y + ball.dy * t

        if expected_y > paddle_y:
            self.dy = 200
        elif expected_y == paddle_y:
            self.dy = 0
        else:
            self.dy = -200
            
        
        diff = math.fabs(expected_y - paddle_y)
        if diff > 200:
            self.dy *= 8
        elif diff > 100:
            self.dy *= 4
        elif diff > 50:
            self.dy *= 2
        elif diff < 10:
            self.dy *= 0

        # print(ball.dy, ball_y, '/', paddle_y, diff)
        # print(ball.dy, dt, t, expected_y)

        super().update(dt)