import pygame
import random
import json
import os

# Initialize Pygame
pygame.init()

# Screen dimensions and margin
WIDTH, HEIGHT = 800, 600
MARGIN = 20  # Margin around the game area
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tile Breaker Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
BORDER_COLOR = (200, 200, 200)  # Border color for game area

# Game settings
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_SIZE = 10
BALL_SPEED = 5
TILE_ROWS = 5
TILE_COLUMNS = 10
TILE_WIDTH = (WIDTH - 2 * MARGIN) // TILE_COLUMNS
TILE_HEIGHT = 30
SCORE_PADDING = 40  # Padding for the score display at the top
LIFE_DISPLAY_SIZE = 20  # Size of life rectangles

# Paddle setup
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball setup
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
ball_dx, ball_dy = BALL_SPEED, -BALL_SPEED

# Tile properties dictionary
tile_types = {
    0: {"color": BLACK, "score": 0},     # No tile
    1: {"color": (255, 0, 0), "score": 10},   # Red tile
    2: {"color": (255, 255, 0), "score": 20}, # Yellow tile
    3: {"color": (0, 255, 255), "score": 30}  # Cyan tile
}

# Tile list, score, and lives
tiles = []
score = 0
lives = 3
highscores = []

# File for storing highscores
HIGHSCORE_FILE = "highscores.json"

# Game states
game_state = "main_menu"  # Options: "main_menu", "playing", "game_over", "highscore"
level = 1

# Font for buttons, messages, and score
font = pygame.font.Font(None, 36)


def load_highscores():
    """Load highscores from a JSON file."""
    global highscores
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as file:
            highscores = json.load(file)
    highscores.sort(key=lambda x: x["score"], reverse=True)


def save_highscore(name, score):
    """Save a new highscore entry."""
    highscores.append({"name": name, "score": score})
    highscores.sort(key=lambda x: x["score"], reverse=True)
    with open(HIGHSCORE_FILE, "w") as file:
        json.dump(highscores, file)


def reset_highscores():
    """Clear highscores after confirmation."""
    global highscores
    confirmation = input("Are you sure you want to reset highscores? (y/n): ")
    if confirmation.lower() == 'y':
        highscores = []
        with open(HIGHSCORE_FILE, "w") as file:
            json.dump(highscores, file)
        print("Highscores reset successfully.")


def reset_ball_and_paddle():
    """Reset the ball and paddle to initial positions."""
    global ball, ball_dx, ball_dy
    paddle.centerx = WIDTH // 2
    ball.x, ball.y = WIDTH // 2, HEIGHT // 2
    ball_dx, ball_dy = BALL_SPEED, -BALL_SPEED


def generate_tiles():
    """Generate tiles randomly for the current level."""
    global tiles
    tile_map = [[random.choice([0, 1, 2, 3]) for _ in range(TILE_COLUMNS)] for _ in range(TILE_ROWS)]
    tiles = [(pygame.Rect(col * TILE_WIDTH + MARGIN, row * TILE_HEIGHT + SCORE_PADDING + MARGIN, TILE_WIDTH, TILE_HEIGHT), tile_map[row][col])
             for row in range(TILE_ROWS) for col in range(TILE_COLUMNS) if tile_map[row][col] != 0]


def draw_main_menu():
    """Draw the main menu with Start, Highscore, and Help buttons."""
    screen.fill(BLACK)
    
    # Draw title
    title_text = font.render("Tile Breaker Game", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_text, title_rect)
    
    # Draw Start button
    start_text = font.render("Start", True, WHITE)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, GRAY, start_rect.inflate(20, 10))
    screen.blit(start_text, start_rect)
    
    # Draw Highscore button
    highscore_text = font.render("Highscore", True, WHITE)
    highscore_rect = highscore_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    pygame.draw.rect(screen, GRAY, highscore_rect.inflate(20, 10))
    screen.blit(highscore_text, highscore_rect)

    return start_rect, highscore_rect


def draw_highscore_screen():
    """Draw the highscore screen with scores, Reset, and Back buttons."""
    screen.fill(BLACK)

    # Display the highscores
    title_text = font.render("Highscores", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 8))
    screen.blit(title_text, title_rect)

    for i, entry in enumerate(highscores[:10]):
        score_text = font.render(f"{i + 1}. {entry['name']} - {entry['score']}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 8 + 50 + i * 30))

    # Draw Reset and Back buttons
    reset_text = font.render("Reset", True, WHITE)
    reset_rect = reset_text.get_rect(center=(WIDTH // 2 - 100, HEIGHT - 50))
    pygame.draw.rect(screen, GRAY, reset_rect.inflate(20, 10))
    screen.blit(reset_text, reset_rect)

    back_text = font.render("Back", True, WHITE)
    back_rect = back_text.get_rect(center=(WIDTH // 2 + 100, HEIGHT - 50))
    pygame.draw.rect(screen, GRAY, back_rect.inflate(20, 10))
    screen.blit(back_text, back_rect)

    return reset_rect, back_rect


def check_victory():
    """Check if all tiles are cleared for level completion."""
    return len(tiles) == 0


def draw_score_and_lives():
    """Draw the current score and lives on the screen."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (MARGIN, MARGIN // 2))

    for i in range(lives):
        life_rect = pygame.Rect(WIDTH - MARGIN - (i + 1) * (LIFE_DISPLAY_SIZE + 5), MARGIN, LIFE_DISPLAY_SIZE, LIFE_DISPLAY_SIZE // 2)
        pygame.draw.rect(screen, BLUE, life_rect)


# Game loop control
running = True
clock = pygame.time.Clock()
load_highscores()

# Main game loop
while running:
    screen.fill(BLACK)

    # Draw the appropriate screen based on the game state
    if game_state == "main_menu":
        start_rect, highscore_rect = draw_main_menu()
    elif game_state == "highscore":
        reset_rect, back_rect = draw_highscore_screen()
    elif game_state == "playing":
        # Draw game area border
        game_area = pygame.Rect(MARGIN, SCORE_PADDING + MARGIN, WIDTH - 2 * MARGIN, HEIGHT - SCORE_PADDING - 2 * MARGIN)
        pygame.draw.rect(screen, BORDER_COLOR, game_area, 2)  # Draw border

        # Paddle movement with mouse
        mouse_x, _ = pygame.mouse.get_pos()
        paddle.centerx = mouse_x
        paddle.clamp_ip(game_area)  # Keep paddle within game area bounds

        # Ball movement
        ball.x += ball_dx
        ball.y += ball_dy

        # Ball collision with walls in the game area
        if ball.left <= MARGIN or ball.right >= WIDTH - MARGIN:
            ball_dx = -ball_dx
        if ball.top <= SCORE_PADDING + MARGIN:
            ball_dy = -ball_dy
        if ball.colliderect(paddle):
            ball_dy = -ball_dy

        # Ball collision with tiles
        for i, (tile, tile_type) in enumerate(tiles):
            if ball.colliderect(tile):
                score += tile_types[tile_type]["score"]  # Increase score based on tile type
                del tiles[i]
                ball_dy = -ball_dy
                break  # Only handle one collision at a time

        # Check for losing a life
        if ball.bottom >= HEIGHT - MARGIN:
            lives -= 1
            if lives > 0:
                reset_ball_and_paddle()
            else:
                game_state = "game_over"

        # Check for victory (all tiles cleared)
        if check_victory():
            level += 1  # Advance to next level
            generate_tiles()  # Generate a new level of tiles
            reset_ball_and_paddle()

        # Draw paddle
        pygame.draw.rect(screen, BLUE, paddle)

        # Draw ball
        pygame.draw.ellipse(screen, WHITE, ball)

        # Draw tiles based on their type
        for tile, tile_type in tiles:
            color = tile_types[tile_type]["color"]  # Get color based on tile type
            pygame.draw.rect(screen, color, tile)

        # Draw score and lives at the top
        draw_score_and_lives()
    elif game_state == "game_over":
        # Prompt for name and save highscore
        player_name = input("Enter your name: ")
        save_highscore(player_name, score)
        game_state = "main_menu"

    # Event handling for the main menu and highscore screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_state == "main_menu" and event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):
                game_state = "playing"
                generate_tiles()
                reset_ball_and_paddle()
                score, lives = 0, 3  # Reset score and lives for new game
            elif highscore_rect.collidepoint(event.pos):
                game_state = "highscore"
        elif game_state == "highscore" and event.type == pygame.MOUSEBUTTONDOWN:
            if back_rect.collidepoint(event.pos):
                game_state = "main_menu"
            elif reset_rect.collidepoint(event.pos):
                reset_highscores()

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
