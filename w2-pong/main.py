import pygame
import sys

WIDTH = 1280
HEIGHT = 720
MAX_FRAME_RATE = 60

class GameMain:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.small_font = pygame.font.Font("./assets/font.ttf", 24)
        self.large_font = pygame.font.Font("./assets/font.ttf", 48)

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def render(self):
        # fill the screen
        self.screen.fill((23, 43, 123))

        # welcome message
        t_welcome = self.small_font.render("welcome to the pong", False, (255, 255, 255))
        text_rect = t_welcome.get_rect(center = (WIDTH/2, 60))
        self.screen.blit(t_welcome, text_rect)

        # paddle -> pygame.Rect(x, y, w, h)
        # right paddle 
        pygame.draw.rect(self.screen, (255, 255, 255), 
                         pygame.Rect(WIDTH-30, HEIGHT-150, 15, 60))
        # left paddle
        pygame.draw.rect(self.screen, (255, 255, 255), 
                         pygame.Rect(30, 150, 15, 60))
        
        # ball
        pygame.draw.rect(self.screen, (255, 255, 255),
                         pygame.Rect(WIDTH/2-6, HEIGHT/2-6, 12, 12))

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