import pygame
import sys

# initialize modules
pygame.init()

WIDTH = 1024
HEIGHT = 768

# main screen surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set title and caption
pygame.display.set_caption("our first game")

# font
small_font = pygame.font.SysFont("Comic Sans MS", 30)
big_font = pygame.font.SysFont("Comic Sans MS", 45)

# text
text1 = "Welcome to Game Dev Course"
text2 = "Hello, World!"

highlight_first_text = True

# make img surface
img = pygame.image.load("IMG_2243.JPG")
img = pygame.transform.scale(img, (400, 400))

while True:
    # process input
    events = pygame.event.get()

    # update
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:      # KEYDOWN = key press / KEYUP = key release
            if event.key == pygame.K_UP:        # K_UP = up arrow
                highlight_first_text = True
            elif event.key == pygame.K_DOWN:    # K_DOWN = down arrow
                highlight_first_text = False

    # render
    screen.fill((0, 204, 204))  # RGB 0-255

    # text surface
    if highlight_first_text:
        text1_render = big_font.render(text1, False, (255, 255, 255))
        text2_render = small_font.render(text2, False, (255, 255, 255))
    else:
        text1_render = small_font.render(text1, False, (255, 255, 255))
        text2_render = big_font.render(text2, False, (255, 255, 255))

    # blit text on the main screen
    screen.blit(text1_render, (100, 100))
    screen.blit(text2_render, (100, 200))

    # blit image on the screen
    screen.blit(img, (300, 300))

    pygame.display.update()
