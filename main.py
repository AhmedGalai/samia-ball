import pygame
from components import Paddle, Ball, generate_tiles, tile_types
from screens import draw_main_menu, draw_highscore_screen, draw_score_and_lives
from utils import load_highscores, save_highscore, reset_highscores

# Initialize Pygame and set up display
pygame.init()
WIDTH, HEIGHT = 800, 600
MARGIN, SCORE_PADDING = 20, 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tile Breaker Game")
font = pygame.font.Font(None, 36)

# Game states and variables
game_state = "main_menu"
running, score, level, lives = True, 0, 1, 3
highscores = load_highscores()
paddle = Paddle(WIDTH // 2, HEIGHT - 50)
ball = Ball(WIDTH // 2, HEIGHT // 2)
tiles = []

# Main game loop
clock = pygame.time.Clock()
while running:
    screen.fill((0, 0, 0))

    # Draw relevant screen based on game state
    if game_state == "main_menu":
        start_rect, highscore_rect = draw_main_menu(screen, font)
    elif game_state == "highscore":
        reset_rect, back_rect = draw_highscore_screen(screen, font, highscores)  # Pass highscores here
    elif game_state == "playing":
        paddle.move(pygame.mouse.get_pos()[0], WIDTH)
        ball.move(WIDTH, HEIGHT, MARGIN, SCORE_PADDING, paddle)
        if ball.check_collision_with_tiles(tiles, tile_types):
            score += ball.last_tile_score
        if ball.bottom_out_of_bounds(HEIGHT, MARGIN):
            lives -= 1
            if lives > 0:
                ball.reset_position(WIDTH // 2, HEIGHT // 2)
            else:
                game_state = "game_over"
        if len(tiles) == 0:  # All tiles cleared
            level += 1
            tiles = generate_tiles()
            ball.reset_position(WIDTH // 2, HEIGHT // 2)
        paddle.draw(screen)
        ball.draw(screen)
        for tile, tile_type in tiles:
            pygame.draw.rect(screen, tile_types[tile_type]["color"], tile)
        draw_score_and_lives(screen, font, score, lives, WIDTH, MARGIN)
    elif game_state == "game_over":
        # Prompt for name and save highscore
        player_name = input("Enter your name: ")
        save_highscore(player_name, score)
        highscores = load_highscores()  # Reload highscores after saving
        game_state = "main_menu"
        score, lives = 0, 3  # Reset score and lives for new game

    # Event handling for main menu and highscore screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_state == "main_menu" and event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):
                game_state, tiles = "playing", generate_tiles()
                paddle.reset_position(WIDTH // 2, HEIGHT - 50)
                ball.reset_position(WIDTH // 2, HEIGHT // 2)
                score, lives = 0, 3
            elif highscore_rect.collidepoint(event.pos):
                game_state = "highscore"
        elif game_state == "highscore" and event.type == pygame.MOUSEBUTTONDOWN:
            if back_rect.collidepoint(event.pos):
                game_state = "main_menu"
            elif reset_rect.collidepoint(event.pos):
                reset_highscores()
                highscores = load_highscores()  # Reload highscores after reset

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
