import pygame
import random
import math
from constant import *
from Ball import Ball

class Paddle:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen

        self.rect = pygame.Rect(x, y, width, height)
        self.dy = 0

    def update(self, dt):
        if self.dy > 0:
            if self.rect.y + self.rect.height < HEIGHT:
                self.rect.y += self.dy*dt
        else:
            if self.rect.y >= 0:
                self.rect.y += self.dy*dt

    def render(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)

class NotSoGoodAIPaddle(Paddle):
    def __init__(self, screen, x, y, width, height):
        super().__init__(screen, x, y, width, height)

    def update(self, dt, ball: Ball):
        if ball.dy > 0:
            self.dy = 150
        else:
            self.dy = -150
        super().update(dt)

class BetterAIPaddle(Paddle):
    def __init__(self, screen, x, y, width, height):
        super().__init__(screen, x, y, width, height)

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

        # print(ball.dy, ball_y, '/', paddle_y, diff)

        super().update(dt)

class BetterAIPaddleV2(Paddle):
    def __init__(self, screen, x, y, width, height):
        super().__init__(screen, x, y, width, height)

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

        # print(ball.dy, ball_y, '/', paddle_y, diff)
        # print(ball.dy, dt, t, expected_y)

        super().update(dt)

class BetterAIPaddleV2Left(Paddle):
    def __init__(self, screen, x, y, width, height):
        super().__init__(screen, x, y, width, height)

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

        # print(ball.dy, ball_y, '/', paddle_y, diff)
        # print(ball.dy, dt, t, expected_y)

        super().update(dt)