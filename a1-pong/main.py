import pygame, sys, random, math

from constant import *
from Ball import Ball
from Paddle import Paddle, WeakAIPaddle, StrongAIPaddle, StrongAIPaddleLeft, PaddleSize
from PowerUp import PowerUp, PowerUpType

class GameMain:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.music_channel = pygame.mixer.Channel(0)
        self.music_channel.set_volume(0.2)
        
        self.sounds_list = {
            'paddle_hit': pygame.mixer.Sound('sounds/paddle_hit.wav'),
            'score': pygame.mixer.Sound('sounds/score.wav'),
            'wall_hit': pygame.mixer.Sound('sounds/wall_hit.wav')
        }

        self.small_font = pygame.font.Font('./font.ttf', 24)
        self.large_font = pygame.font.Font('./font.ttf', 48)
        self.score_font = pygame.font.Font('./font.ttf', 96)

        self.player1_score = 0
        self.player2_score = 0

        self.serving_player = 1
        self.winning_player = 0
        self.last_hit_player = 1

        player1_color = (0, 255, 255)   # neon blue
        player2_color = (255, 20, 147)  # neon pink
        self.player1 = StrongAIPaddleLeft(self.screen, 30, 90, PADDLE_WIDTH, PaddleSize.MEDIUM, player1_color)
        self.player2 = StrongAIPaddle(self.screen, WIDTH - 30, HEIGHT - 90, PADDLE_WIDTH, PaddleSize.MEDIUM, player2_color)

        self.ball = Ball(self.screen, WIDTH/2 - 6, HEIGHT/2 - 6, BALL_SIZE, BALL_SIZE)

        self.powerups = []
        self.game_state = 'start'

        # Timer for generating power-ups/power-downs
        self.powerup_timer = 0

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_state == 'start':
                        self.game_state = 'serve'
                    elif self.game_state == 'serve':
                        self.game_state = 'play'
                    elif self.game_state == 'done':
                        self.game_state = 'serve'
                        self.ball.Reset()

                        self.player1_score = 0
                        self.player2_score = 0

                        self.player1.Reset() 
                        self.player2.Reset() 

                        if self.winning_player == 1:
                            self.serving_player = 2
                        else:
                            self.serving_player = 1

        if self.game_state == 'serve':
            self.ball.dy = random.uniform(-150, 150)
            if self.serving_player == 1:
                self.ball.dx = random.uniform(420, 600)
            else:
                self.ball.dx = -random.uniform(420, 600)

        elif self.game_state == 'play':
            self.check_collisions()
            self.update_powerups(dt)

        if self.game_state == 'play':
            self.ball.update(dt)

        self.player1.update(dt, self.ball)
        self.player2.update(dt, self.ball)

    def check_collisions(self):
        # ball hit player 1 paddle
        if self.ball.Collides(self.player1):
            self.ball.dx = -self.ball.dx * 1.03
            self.ball.rect.x = self.player1.rect.x + 15

            if self.ball.dy < 0:
                self.ball.dy = -random.uniform(30, 450)
            else:
                self.ball.dy = random.uniform(30, 450)

            self.music_channel.play(self.sounds_list['paddle_hit'])
            self.last_hit_player = 1

        # ball hit player 2 paddle
        if self.ball.Collides(self.player2):
            self.ball.dx = -self.ball.dx * 1.03
            self.ball.rect.x = self.player2.rect.x - BALL_SIZE
            if self.ball.dy < 0:
                self.ball.dy = -random.uniform(30, 450)
            else:
                self.ball.dy = random.uniform(30, 450)

            self.music_channel.play(self.sounds_list['paddle_hit'])
            self.last_hit_player = 2

        # ball hit top wall
        if self.ball.rect.y <= 0:
            self.ball.rect.y = 0
            self.ball.dy = -self.ball.dy
            self.music_channel.play(self.sounds_list['wall_hit'])

        # ball hit bottom wall
        if self.ball.rect.y >= HEIGHT - BALL_SIZE:
            self.ball.rect.y = HEIGHT - BALL_SIZE
            self.ball.dy = -self.ball.dy
            self.music_channel.play(self.sounds_list['wall_hit'])

        # ball hit player 1 goal
        if self.ball.rect.x < 0:
            self.serving_player = 1
            self.player2_score += 1
            self.music_channel.play(self.sounds_list['score'])
            if self.player2_score==WINNING_SCORE:
                self.winning_player=2
                self.game_state='done'
            else:
                self.game_state = 'serve'
                self.ball.Reset()
        
        # ball hit player 2 goal
        if self.ball.rect.x > WIDTH:
            self.serving_player = 2
            self.player1_score += 1
            self.music_channel.play(self.sounds_list['score'])
            if self.player1_score==WINNING_SCORE:
                self.winning_player=1
                self.game_state='done'
            else:
                self.game_state = 'serve'
                self.ball.Reset()    

        for powerup in self.powerups:
            if powerup.active and self.ball.rect.colliderect(powerup.rect):
                # self.apply_powerup(powerup)
                print(self.last_hit_player, powerup.effect)
                if self.last_hit_player == 1:
                    self.apply_powerup(powerup, self.player1)
                elif self.last_hit_player == 2:
                    self.apply_powerup(powerup, self.player2)
                powerup.active = False

    def update_powerups(self, dt):
        self.powerup_timer += dt
        if self.powerup_timer > random.uniform(2, 10):  
            self.spawn_powerup()
            self.powerup_timer = 0

        # for powerup in self.powerups:
        #     powerup.update(dt)

    def spawn_powerup(self):
        x = random.randint(POWERUPS_SIZE, WIDTH - POWERUPS_SIZE)
        y = random.randint(POWERUPS_SIZE, HEIGHT - POWERUPS_SIZE)
        
        self.powerups.append(PowerUp(self.screen, x, y, POWERUPS_SIZE, POWERUPS_SIZE))

    def apply_powerup(self, powerup, player):

        # Paddle Size
        current_size = PaddleSize(self.player1.rect.height)

        if powerup.effect == PowerUpType.INCREASE_PADDLE:
            if current_size != PaddleSize.HUGE:
                new_size = PaddleSize(min(current_size.value + 20, PaddleSize.HUGE.value))
                self.player1.rect.height = new_size.value
        elif powerup.effect == PowerUpType.DECREASE_PADDLE:
            if current_size != PaddleSize.TINY:
                new_size = PaddleSize(max(current_size.value - 20, PaddleSize.TINY.value))
                self.player1.rect.height = new_size.value

        # Ball Speed
        elif powerup.effect == PowerUpType.INCREASE_BALL_SPEED:
            self.ball.dx *= 1.5
            self.ball.dy *= 1.5
            print(self.ball.dx, self.ball.dy)
        elif powerup.effect == PowerUpType.DECREASE_BALL_SPEED:
            if math.fabs(self.ball.dx) > 150 or math.fabs(self.ball.dy) > 150:
                self.ball.dx *= 0.6
                self.ball.dy *= 0.6
            print(self.ball.dx, self.ball.dy)

    def render(self):
        self.screen.fill((40, 45, 52))

        if self.game_state == 'start':
            t_welcome = self.small_font.render("Welcome to Pong!", False, (255, 255, 255))
            text_rect = t_welcome.get_rect(center=(WIDTH / 2, 30))
            self.screen.blit(t_welcome, text_rect)

            t_press_enter_begin = self.small_font.render('Press Enter to begin!', False, (255, 255, 255))
            text_rect = t_press_enter_begin.get_rect(center=(WIDTH / 2, 60))
            self.screen.blit(t_press_enter_begin, text_rect)
        elif self.game_state == 'serve':
            t_serve = self.small_font.render("player" + str(self.serving_player) + "'s serve!", False, (255, 255, 255))
            text_rect = t_serve.get_rect(center=(WIDTH / 2, 30))
            self.screen.blit(t_serve, text_rect)

            t_enter_serve = self.small_font.render("Press Enter to serve!", False, (255, 255, 255))
            text_rect = t_enter_serve.get_rect(center=(WIDTH / 2, 60))
            self.screen.blit(t_enter_serve, text_rect)
        elif self.game_state == 'done':
            t_win = self.large_font.render("player" + str(self.winning_player) + " wins!", False, (255, 255, 255))
            text_rect = t_win.get_rect(center=(WIDTH / 2, 30))
            self.screen.blit(t_win, text_rect)

            t_restart = self.small_font.render("Press Enter to restart", False, (255, 255, 255))
            text_rect = t_restart.get_rect(center=(WIDTH / 2, 70))
            self.screen.blit(t_restart, text_rect)

        # right paddle
        self.player2.render()

        # left paddle
        self.player1.render()

        # ball
        self.ball.render()

        # render power-ups
        for powerup in self.powerups:
            powerup.render()

        # render score    
        self.DisplayScore()

    def DisplayScore(self):
        self.t_p1_score = self.score_font.render(str(self.player1_score), False, (255, 255, 255))
        self.t_p2_score = self.score_font.render(str(self.player2_score), False, (255, 255, 255))
        self.screen.blit(self.t_p1_score, (WIDTH/2 - 150, HEIGHT/3))
        self.screen.blit(self.t_p2_score, (WIDTH / 2 + 120, HEIGHT / 3))


if __name__ == '__main__':
    clock = pygame.time.Clock()
    game = GameMain()

    while True:
        dt = clock.tick(60) / 1000
        events = pygame.event.get()
        game.update(dt, events)
        game.render()
        pygame.display.update()
