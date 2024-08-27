import pygame
import random
import math
from constant import *
from enum import Enum, auto

class PowerUpType(Enum):
    INCREASE_PADDLE = auto()
    DECREASE_PADDLE = auto()
    INCREASE_BALL_SPEED = auto()
    DECREASE_BALL_SPEED = auto()

POWERUP_COLORS = {
    PowerUpType.INCREASE_PADDLE: (0, 255, 0),  # Green
    PowerUpType.DECREASE_PADDLE: (255, 0, 0),  # Red
    PowerUpType.INCREASE_BALL_SPEED: (0, 0, 255),   # Blue
    PowerUpType.DECREASE_BALL_SPEED: (255, 255, 0), # Yellow
    # Add more effect types and their corresponding colors here
}

class PowerUp:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.effect = random.choice(list(PowerUpType))
        # self.effect = PowerUpType.INCREASE_BALL_SPEED
        self.active = True

    def render(self):
        if self.active:
            color = POWERUP_COLORS.get(self.effect, (255, 255, 255))  # Default to white if effect type not found
            pygame.draw.rect(self.screen, color, self.rect)

    def update(self, dt):
        pass  # Power-ups can move or have animations if needed
