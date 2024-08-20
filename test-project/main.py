import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
TILE_SIZE = 80
WIDTH = TILE_SIZE * 10
HEIGHT = TILE_SIZE * 8
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Game")

# Colors
WHITE = (255, 255, 255)

# Load assets
grass_img = pygame.image.load('assets/tiles/grass.png')
grass_img = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
water_img = pygame.image.load('assets/tiles/water.png')
water_img = pygame.transform.scale(water_img, (TILE_SIZE, TILE_SIZE))
player_sprite_sheet = pygame.image.load('assets/player/Player.png')

# Define the map (0 = grass, 1 = water)
tile_map = [
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# Player settings
ORIGINAL_PLAYER_WIDTH, ORIGINAL_PLAYER_HEIGHT = 32, 32
DISPLAY_PLAYER_WIDTH, DISPLAY_PLAYER_HEIGHT = 80, 80
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
player_anim_index = 0

# Load and scale player frames
player_frames = [
    pygame.transform.scale(player_sprite_sheet.subsurface(pygame.Rect(0, 0, ORIGINAL_PLAYER_WIDTH, ORIGINAL_PLAYER_HEIGHT)), (DISPLAY_PLAYER_WIDTH, DISPLAY_PLAYER_HEIGHT)),
    pygame.transform.scale(player_sprite_sheet.subsurface(pygame.Rect(32, 0, ORIGINAL_PLAYER_WIDTH, ORIGINAL_PLAYER_HEIGHT)), (DISPLAY_PLAYER_WIDTH, DISPLAY_PLAYER_HEIGHT)),
    pygame.transform.scale(player_sprite_sheet.subsurface(pygame.Rect(64, 0, ORIGINAL_PLAYER_WIDTH, ORIGINAL_PLAYER_HEIGHT)), (DISPLAY_PLAYER_WIDTH, DISPLAY_PLAYER_HEIGHT)),
]
# Draw the map
def draw_map():
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            if tile == 0:
                WIN.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == 1:
                WIN.blit(water_img, (x * TILE_SIZE, y * TILE_SIZE))

# Draw the map
def draw_map():
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            if tile == 0:
                WIN.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == 1:
                WIN.blit(water_img, (x * TILE_SIZE, y * TILE_SIZE))

# Game loop
def main():
    global player_x, player_y, player_anim_index
    clock = pygame.time.Clock()
    running = True

    # Animation settings
    anim_counter = 0
    anim_speed = 10  # The higher the value, the slower the animation

    while running:
        clock.tick(60)  # Set FPS to 60

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Key handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += player_speed

        # Animate player
        anim_counter += 1
        if anim_counter >= anim_speed:
            player_anim_index = (player_anim_index + 1) % len(player_frames)
            anim_counter = 0

        # Draw everything
        WIN.fill(WHITE)
        draw_map()
        WIN.blit(player_frames[player_anim_index], (player_x, player_y))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()