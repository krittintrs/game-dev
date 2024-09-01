from enum import Enum
import pygame, sys, random, math

from constant import *
from Ball import Ball
from Paddle import Paddle, WeakAIPaddle, StrongAIPaddle, StrongAIPaddleLeft, PaddleSize
from PowerUp import PowerUp, PowerUpType

PLAYER_1_BLINK_EVENT = pygame.USEREVENT + 1
PLAYER_2_BLINK_EVENT = pygame.USEREVENT + 2
BALL_BLINK_EVENT = pygame.USEREVENT + 3

class GameState(Enum):
    START = 'start'
    SERVE = 'serve'
    PLAY = 'play'
    DONE = 'done'

class Player(Enum):
    PLAYER_1 = 1
    PLAYER_2 = 2
    
class AIType(Enum):
    WEAK = 'weak'
    STRONG = 'strong'

class GameMain:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.music_channel = pygame.mixer.Channel(0)
        self.music_channel.set_volume(0.2)
        
        self.sounds_list = {
            'paddle_hit': pygame.mixer.Sound('sounds/paddle_hit.wav'),
            'score': pygame.mixer.Sound('sounds/score.wav'),
            'wall_hit': pygame.mixer.Sound('sounds/wall_hit.wav'),
            'increase_paddle': pygame.mixer.Sound('sounds/increase_paddle.wav'),
            'decrease_paddle': pygame.mixer.Sound('sounds/decrease_paddle.wav'),
            'speed_boost': pygame.mixer.Sound('sounds/speed_boost.wav'),
            'split_ball': pygame.mixer.Sound('sounds/split_ball.wav'),
        }

        self.small_font = pygame.font.Font('./font.ttf', 24)
        self.large_font = pygame.font.Font('./font.ttf', 48)
        self.score_font = pygame.font.Font('./font.ttf', 96)

        self.player1_score = 0
        self.player2_score = 0

        self.serving_player = Player.PLAYER_1
        self.winning_player = 0
        self.last_hit_player = Player.PLAYER_1

        self.player1_color = (0, 255, 255)   # neon blue
        self.player2_color = (255, 20, 147)  # neon pink
        # self.player1 = Paddle(self.screen, 30, 90, PADDLE_WIDTH, PaddleSize.MEDIUM, player1_color)
        self.player1 = StrongAIPaddleLeft(self.screen, 30, 90, PADDLE_WIDTH, PaddleSize.MEDIUM, self.player1_color)

        self.weak_ai = WeakAIPaddle(self.screen, WIDTH - 30, HEIGHT - 90, PADDLE_WIDTH, PaddleSize.MEDIUM, self.player2_color)
        self.strong_ai = StrongAIPaddle(self.screen, WIDTH - 30, HEIGHT - 90, PADDLE_WIDTH, PaddleSize.MEDIUM, self.player2_color)
        
        self.current_ai_type = AIType.WEAK
        self.player2 = self.get_current_ai()

        self.ball = Ball(self.screen, WIDTH/2 - 6, HEIGHT/2 - 6, BALL_SIZE, BALL_SIZE)

        self.powerups = []
        self.game_state = GameState.START

        self.original_ball_speed = (self.ball.dx, self.ball.dy)
        self.ball_speed_boost_active = False
    
        # Timer for generating power-ups/power-downs
        self.powerup_timer = 0

    def get_current_ai(self):
        if self.current_ai_type == AIType.WEAK:
            return self.weak_ai
        elif self.current_ai_type == AIType.STRONG:
            return self.strong_ai
        
    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_state == GameState.START:
                        self.game_state = GameState.SERVE
                    elif self.game_state == GameState.SERVE:
                        self.game_state = GameState.PLAY
                    elif self.game_state == GameState.DONE:
                        self.game_state = GameState.SERVE
                        self.reset_field()
                        if self.winning_player == Player.PLAYER_1:
                            self.serving_player = Player.PLAYER_2
                        else:
                            self.serving_player = Player.PLAYER_1
            
            if event.type == PLAYER_1_BLINK_EVENT:
                if self.blink_count < 4:
                    if self.blink_count % 2 == 0:
                        glow_color = (255, 255, 255)
                        inner_color = (255, 255, 255)
                    else:
                        glow_color = self.player1_color
                        inner_color = (0, 0, 0)

                    self.player1.glow_color = glow_color
                    self.player1.inner_color = inner_color

                    self.blink_count += 1
                else:
                    self.player1.glow_color = self.player1_color
                    self.player1.inner_color = (0, 0, 0)
                    pygame.time.set_timer(PLAYER_1_BLINK_EVENT, 0)  # Stop the timer

            if event.type == PLAYER_2_BLINK_EVENT:
                if self.blink_count < 4:
                    if self.blink_count % 2 == 0:
                        glow_color = (255, 255, 255)
                        inner_color = (255, 255, 255)
                    else:
                        glow_color = self.player2_color
                        inner_color = (0, 0, 0)

                    self.player2.glow_color = glow_color
                    self.player2.inner_color = inner_color

                    self.blink_count += 1
                else:
                    self.player2.glow_color = self.player2_color
                    self.player2.inner_color = (0, 0, 0)
                    pygame.time.set_timer(PLAYER_2_BLINK_EVENT, 0)  # Stop the timer

            if event.type == BALL_BLINK_EVENT:
                self.ball.color = (255, 255, 255)  # Revert the ball color to white
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Stop the timer
                if self.ball_speed_boost_active:
                    self.ball.dx = self.ball.dx / SPEED_BOOST_VALUE
                    self.ball.dy = self.ball.dy / SPEED_BOOST_VALUE
                    self.ball_speed_boost_active = False
                # print(f'SPEED: ({self.ball.dx}, {self.ball.dy})')

        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.player1.dy = -PADDLE_SPEED
        elif key[pygame.K_s]:
            self.player1.dy = PADDLE_SPEED
        else:
            self.player1.dy = 0       
        
        if self.game_state == GameState.SERVE:
            self.ball.dy = random.uniform(-150, 150)
            if self.serving_player == Player.PLAYER_1:
                self.ball.dx = random.uniform(420, 600)
            else:
                self.ball.dx = -random.uniform(420, 600)

        elif self.game_state == GameState.PLAY:
            self.check_collisions()
            self.update_powerups(dt)
            self.ball.update(dt)

        # self.player1.update(dt)
        self.player1.update(dt, self.ball)
        self.player2.update(dt, self.ball)

    def reset_field(self):
        self.ball.Reset()
        self.player1.Reset() 
        self.player2.Reset() 
        self.player1_score = 0
        self.player2_score = 0
        self.powerups = []

    def render(self):
        self.screen.fill((40, 45, 52))

        if self.game_state == GameState.START:
            t_welcome = self.small_font.render("Welcome to Pong!", False, (255, 255, 255))
            text_rect = t_welcome.get_rect(center=(WIDTH / 2, 30))
            self.screen.blit(t_welcome, text_rect)

            t_press_enter_begin = self.small_font.render('Press Enter to begin!', False, (255, 255, 255))
            text_rect = t_press_enter_begin.get_rect(center=(WIDTH / 2, 60))
            self.screen.blit(t_press_enter_begin, text_rect)

        elif self.game_state == GameState.SERVE:
            t_ai_mode = self.small_font.render(str(self.current_ai_type.value).upper() + " AI Mode", False, (255, 255, 255))
            text_rect = t_ai_mode.get_rect(center=(WIDTH / 2, 30))
            self.screen.blit(t_ai_mode, text_rect)

            t_serve = self.small_font.render("Player " + str(self.serving_player.value) + "'s serve!", False, (255, 255, 255))
            text_rect = t_serve.get_rect(center=(WIDTH / 2, 60))
            self.screen.blit(t_serve, text_rect)

            t_enter_serve = self.small_font.render("Press Enter to serve!", False, (255, 255, 255))
            text_rect = t_enter_serve.get_rect(center=(WIDTH / 2, 90))
            self.screen.blit(t_enter_serve, text_rect)

        elif self.game_state == GameState.DONE:
            t_win = self.large_font.render("Player " + str(self.winning_player.value) + " wins!", False, (255, 255, 255))
            text_rect = t_win.get_rect(center=(WIDTH / 2, 30))
            self.screen.blit(t_win, text_rect)

            t_restart = self.small_font.render("Press Enter to restart", False, (255, 255, 255))
            text_rect = t_restart.get_rect(center=(WIDTH / 2, 70))
            self.screen.blit(t_restart, text_rect)

        # render paddle
        self.player1.render()
        self.player2.render()

        # render ball
        self.ball.render()

        # render power-ups
        for powerup in self.powerups:
            powerup.render()

        # render score    
        self.DisplayScore()

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
            self.last_hit_player = Player.PLAYER_1

        # ball hit player 2 paddle
        if self.ball.Collides(self.player2):
            self.ball.dx = -self.ball.dx * 1.03
            self.ball.rect.x = self.player2.rect.x - BALL_SIZE
            if self.ball.dy < 0:
                self.ball.dy = -random.uniform(30, 450)
            else:
                self.ball.dy = random.uniform(30, 450)

            self.music_channel.play(self.sounds_list['paddle_hit'])
            self.last_hit_player = Player.PLAYER_2

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
            if self.player2_score == WINNING_SCORE:
                # player lose to AI
                self.winning_player = Player.PLAYER_2
                self.game_state = GameState.DONE
                # change to weak AI
                self.current_ai_type = AIType.WEAK
                self.player2 = self.get_current_ai()
            else:
                self.game_state = GameState.SERVE
                self.ball.Reset()
        
        # ball hit player 2 goal
        if self.ball.rect.x > WIDTH:
            self.serving_player = 2
            self.player1_score += 1
            self.music_channel.play(self.sounds_list['score'])
            if self.player1_score == WINNING_SCORE:
                # player win against AI
                self.winning_player = Player.PLAYER_1
                self.game_state = GameState.DONE
                # if win against weak AI, change to strong AI
                if self.current_ai_type == AIType.WEAK:
                    self.current_ai_type = AIType.STRONG
                else:
                    self.current_ai_type = AIType.WEAK
                self.player2 = self.get_current_ai()
            else:
                self.game_state = GameState.SERVE
                self.ball.Reset()    

        # ball hit powerups
        for powerup in self.powerups:
            if powerup.active and self.ball.rect.colliderect(powerup.rect):
                # self.apply_powerup(powerup)
                if self.last_hit_player == Player.PLAYER_1:
                    self.apply_powerup(powerup, self.player1)
                elif self.last_hit_player == Player.PLAYER_2:
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
        max_attempts = 100  # Set a limit to avoid infinite loops
        attempt = 0
        
        while attempt < max_attempts:
            x = random.randint(POWERUPS_SIZE, WIDTH - POWERUPS_SIZE)
            y = random.randint(POWERUPS_SIZE, HEIGHT - POWERUPS_SIZE)
            
            new_rect = pygame.Rect(x, y, POWERUPS_SIZE, POWERUPS_SIZE)
            
            # Check for collision with existing power-ups
            collision = any(new_rect.colliderect(powerup.rect) for powerup in self.powerups)
            
            if not collision:
                self.powerups.append(PowerUp(self.screen, x, y, POWERUPS_SIZE, POWERUPS_SIZE))
                break  # Exit the loop once a valid position is found
            
            attempt += 1
        
        if attempt == max_attempts:
            print("Warning: Could not find a non-colliding position for the power-up.")

    def apply_powerup(self, powerup: PowerUp, player):
        # Paddle Size
        current_size = PaddleSize(player.rect.height)
        if powerup.effect == PowerUpType.INCREASE_PADDLE:
            self.music_channel.play(self.sounds_list['increase_paddle'])
            if current_size != PaddleSize.HUGE:
                new_size = PaddleSize(min(current_size.value + 40, PaddleSize.HUGE.value))
                player.rect.height = new_size.value
            self.blink_count = 0
            if player == self.player1:
                pygame.time.set_timer(PLAYER_1_BLINK_EVENT, POWERUPS_TIMER) 
            elif player == self.player2:
                pygame.time.set_timer(PLAYER_2_BLINK_EVENT, POWERUPS_TIMER) 

        elif powerup.effect == PowerUpType.DECREASE_PADDLE:
            self.music_channel.play(self.sounds_list['decrease_paddle'])
            if current_size != PaddleSize.TINY:
                new_size = PaddleSize(max(current_size.value - 40, PaddleSize.TINY.value))
                player.rect.height = new_size.value
            self.blink_count = 0
            if player == self.player1:
                pygame.time.set_timer(PLAYER_1_BLINK_EVENT, POWERUPS_TIMER) 
            elif player == self.player2:
                pygame.time.set_timer(PLAYER_2_BLINK_EVENT, POWERUPS_TIMER)

        # Ball Speed
        elif powerup.effect == PowerUpType.SPEED_BOOST:
            # print('\nBOOSTING!')
            # print(f'OLD SPEED: ({self.ball.dx}, {self.ball.dy})')
            self.music_channel.play(self.sounds_list['speed_boost'])
            self.ball_speed_boost_active = True
            self.ball.dx *= SPEED_BOOST_VALUE
            self.ball.dy *= SPEED_BOOST_VALUE
            self.ball.color = (255, 0, 0)  # red
            self.blink_count = 0
            pygame.time.set_timer(BALL_BLINK_EVENT, SPEED_BOOST_TIMER) 
            # print(f'NEW SPEED: ({self.ball.dx}, {self.ball.dy})\n')
            

        # Split Ball
        elif powerup.effect == PowerUpType.SPLIT_BALL:
            self.music_channel.play(self.sounds_list['split_ball'])
            pass

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
