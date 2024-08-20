import pygame
import sys
import random

WIDTH = 1280
HEIGHT = 720

PADDLE_SPEED = 600

MAX_FRAME_RATE = 60

class GameMain:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.small_font = pygame.font.Font("./assets/font.ttf", 24)
        self.large_font = pygame.font.Font("./assets/font.ttf", 48)

        # y location of paddles
        self.player1_y = 90
        self.player2_y = HEIGHT - 150

        # ball location
        self.ball_x = 0
        self.ball_y = 0
        self.ball_dx = 0
        self.ball_dy = 0
        self.ResetBall()

        self.game_state = 'start'
    
    def ResetBall(self):
        self.ball_x = WIDTH/2 - 6
        self.ball_y = HEIGHT/2 - 6
        self.ball_dx = random.choice([-300, 300])   # randomly choose between go left or right
        self.ball_dy = random.randint(-150, 150)    # randomly select y speed

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
                        self.ResetBall()

        # continuous input -> NOT IN FOR LOOP!!!
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.player1_y -= PADDLE_SPEED * dt
        elif key[pygame.K_s]:
            self.player1_y += PADDLE_SPEED * dt 
        if key[pygame.K_UP]:
            self.player2_y -= PADDLE_SPEED * dt
        elif key[pygame.K_DOWN]:
            self.player2_y += PADDLE_SPEED * dt 

        if self.game_state == 'play':
            self.ball_x += self.ball_dx * dt
            self.ball_y += self.ball_dy * dt

    def render(self):
        # fill the screen
        self.screen.fill((23, 43, 123))

        # welcome message
        t_welcome = self.small_font.render("welcome to the pong", False, (255, 255, 255))
        text_rect = t_welcome.get_rect(center = (WIDTH/2, 60))
        self.screen.blit(t_welcome, text_rect)

        # paddle -> pygame.Rect(x, y, w, h)
        # left paddle
        pygame.draw.rect(self.screen, (255, 255, 255), 
                         pygame.Rect(30, self.player1_y, 15, 60))
        
        # right paddle 
        pygame.draw.rect(self.screen, (255, 255, 255), 
                         pygame.Rect(WIDTH-30, self.player2_y, 15, 60))
        
        # ball
        pygame.draw.rect(self.screen, (255, 255, 255),
                         pygame.Rect(self.ball_x, self.ball_y, 12, 12))

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