import pygame
import random

# Tile properties dictionary
tile_types = {
    0: {"color": (0, 0, 0), "score": 0},
    1: {"color": (255, 0, 0), "score": 10},
    2: {"color": (255, 255, 0), "score": 20},
    3: {"color": (0, 255, 255), "score": 30}
}

# Generate tiles for a level
def generate_tiles(rows=5, columns=10, width=800, margin=20, score_padding=40):
    TILE_WIDTH = (width - 2 * margin) // columns
    TILE_HEIGHT = 30
    tile_map = [[random.choice([0, 1, 2, 3]) for _ in range(columns)] for _ in range(rows)]
    print(tile_map)
    return [(pygame.Rect(col * TILE_WIDTH + margin, row * TILE_HEIGHT + score_padding + margin, TILE_WIDTH, TILE_HEIGHT), tile_map[row][col])
            for row in range(rows) for col in range(columns) if tile_map[row][col] != 0]


# Paddle class
class Paddle:
    def __init__(self, x, y, width=100, height=10, color=(0, 0, 255)):
        self.rect = pygame.Rect(x - width // 2, y, width, height)
        self.color = color

    def move(self, x, screen_width):
        self.rect.centerx = x
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_width))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def reset_position(self, x, y):
        self.rect.centerx = x
        self.rect.y = y


# Ball class
class Ball:
    def __init__(self, x, y, size=10, speed=5, color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, size, size)
        self.dx = speed
        self.dy = -speed
        self.color = color
        self.last_tile_score = 0

    def move(self, screen_width, screen_height, margin, score_padding, paddle):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce on screen borders
        if self.rect.left <= margin or self.rect.right >= screen_width - margin:
            self.dx = -self.dx
        if self.rect.top <= score_padding + margin:
            self.dy = -self.dy
        if self.rect.colliderect(paddle.rect):
            self.dy = -self.dy

    def check_collision_with_tiles(self, tiles, tile_types):
        for i, (tile, tile_type) in enumerate(tiles):
            if self.rect.colliderect(tile):
                self.last_tile_score = tile_types[tile_type]["score"]
                del tiles[i]
                self.dy = -self.dy
                return True
        return False

    def bottom_out_of_bounds(self, screen_height, margin):
        return self.rect.bottom >= screen_height - margin

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def reset_position(self, x, y):
        self.rect.center = (x, y)
