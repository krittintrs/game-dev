import pygame
import sys
import random

from constant import *
from Ball import Ball
from Paddle import Paddle

class GameMain:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.small_font = pygame.font.Font("./assets/font.ttf", 24)
        self.large_font = pygame.font.Font("./assets/font.ttf", 48)

        self.player1 = Paddle(self.screen, 30, 90, 15, 60)
        self.player2 = Paddle(self.screen, WIDTH-30, HEIGHT-90, 15, 60)

        self.ball = Ball(self.screen, WIDTH/2-6, HEIGHT/2-6, 12, 12)

        self.game_state = 'start'

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_state == 'start':  # start -> ball not move
                        self.game_state = 'play'    # play  -> ball move
                    else:
                        self.game_state = 'start'
                        self.ball.Reset()

        # continuous input -> NOT IN FOR LOOP!!!
        key = pygame.key.get_pressed()

        # player 1
        if key[pygame.K_w]:
            self.player1.dy = -PADDLE_SPEED
        elif key[pygame.K_s]:
            self.player1.dy = PADDLE_SPEED
        else:
            self.player1.dy = 0

        # player 2
        if key[pygame.K_UP]:
            self.player2.dy = -PADDLE_SPEED
        elif key[pygame.K_DOWN]:
            self.player2.dy = PADDLE_SPEED
        else:
            self.player2.dy = 0

        if self.game_state == 'play':
            self.ball.update(dt)

        self.player1.update(dt)
        self.player2.update(dt)

    def render(self):
        # fill the screen
        self.screen.fill((38, 125, 166))

        # welcome message
        t_welcome = self.small_font.render("welcome to the pong", False, (255, 255, 255))
        text_rect = t_welcome.get_rect(center = (WIDTH/2, 60))
        self.screen.blit(t_welcome, text_rect)

        self.ball.render()
        self.player1.render()
        self.player2.render()

if __name__ == '__main__':
    main = GameMain()
    clock = pygame.time.Clock()

    while True:
        pygame.display.set_caption(f"Pong game running {int(clock.get_fps())} FPS")

        # elapsed time from the last frame
        dt = clock.tick(MAX_FRAME_RATE)/1000.0

        # process input
        events = pygame.event.get()
        main.update(dt, events)
        main.render()

        pygame.display.update()