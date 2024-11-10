
import pygame
import random

# Tile properties dictionary with probabilities
tile_types = { # implement hardness
    3: {"name": "empty", "color": (0, 0, 0), "score": 0, "probability": 0.5, "hardness":0}, #### remove ?
    1: {"name": "explosive", "color": (255, 0, 0), "score": 5, "probability": 0.1,"hardness":1},  
    2: {"name": "unbreakable", "color": (255, 255, 0), "score": 0, "probability": 0.05,"hardness":None},
    0: {"name": "basic", "color": (0, 255, 255), "score": 1, "probability": 0.25,"hardness":1}, ##### diversify basic colors
    4: {"name": "hard", "color": (255, 255, 255), "score": 10, "probability": 0.05,"hardness":2}, #### adjust saturation/value with hits
}

paddle_properties = {
    0: {"name":"pistol"}, ############ left clicking launches bullets upwards to the tiles
    1: {"name":"magnetic"}, ############## holds ball until left click (level start should be always like this)
}

ball_properties = {
    0: {"name":"fire"}, ############## destroys tiles in 8-er Nachbarschaft of ball position when collision with tiles happens (can destroy unbreakable tiles)
    1: {"name":"sharp"}, ############# penetrates tiles without affecting ball movement (can destroy unbreakable tiles)
}

modifiers = {
    0 : {"name":"sharp_ball"}, #### add sharp property to ball
    1 : {"name":"fire_ball"}, #### add fite property to ball
    2 : {"name":"slow_ball"}, ### ball_speed = max(min_speed,ball_speed * 0.75)
    3 : {"name":"fast_ball"}, ### ball_speed = min(max_speed,ball_speed * 1.25)
    4 : {"name":"multiply_ball"}, ### make 2 copies of each of the current balls along with their properties
    5 : {"name":"shrink_paddle"}, ### paddle_size = max(min_size,paddle_size * 0.75)
    6 : {"name":"grow_paddle"}, ### paddle_size = min(max_size,paddle_size * 1.25)
    7 : {"name":"pistol_paddle"}, #### add pistol property to paddle
    8 : {"name":"magnetic_paddle"}, #### add magnetic property to paddle
    9 : {"name":"extra_life"}, #### gain 1 life
    10 : {"name":"lose_life"},  ##### lose 1 life (refresh state to ball being held by paddle)
    11 : {"name":"lower_tiles"}, ##### lower remaining tiles by 1 level (y axis)
    12 : {"name":"explode_tiles"} #### explodes all explosive tiles
    13 : {"name":"skip_level"} ##### go to next level
    14 : {"name":"soften_tiles"} ##### unbreakable tiles become breakable, hard tiles become basic ....
    15 : {"name":"more_explosives"} ##### increase explosive tiles
    16 : {"name":"2x_score"} ##### double score for --:--
}

# Function to handle the explosion effect by marking adjacent tiles for removal
def apply_explosion_effect(tile_index, tiles, columns, rows, tiles_to_remove, neighborhood=[(-1, 0), (1, 0), (0, -1), (0, 1)]):
    x, y = tile_index % columns, tile_index // columns
    adjacent_indices = [
        (x + dx, y + dy)
        for dx, dy in neighborhood
        if 0 <= x + dx < columns and 0 <= y + dy < rows
    ]

    for adj_x, adj_y in adjacent_indices:
        adj_index = adj_y * columns + adj_x
        if adj_index < len(tiles):
            _, tile_type = tiles[adj_index]
            tiles_to_remove.add(adj_index)  # Mark adjacent tiles for removal

def fire_ball_collision(tile_index, tiles, columns, rows, tiles_to_remove):
    return apply_explosion_effect(tile_index, tiles, columns, rows, tiles_to_remove, [(-1, 0), (1, 0), (0, -1), (0, 1),(1,1),(1,-1),(-1,1),(-1,-1)])

# Generate tiles for a level
def generate_tiles(rows=5, columns=10, width=800, margin=20, score_padding=40):
    TILE_WIDTH = (width - 2 * margin) // columns
    TILE_HEIGHT = 30

    # Generate a list of tile types weighted by their probabilities
    tile_choices = [tile_type for tile_type, properties in tile_types.items()
                    for _ in range(int(properties["probability"] * 100))]

    tile_map = [[random.choice(tile_choices) for _ in range(columns)] for _ in range(rows)]
    return [(pygame.Rect(col * TILE_WIDTH + margin, row * TILE_HEIGHT + score_padding + margin, TILE_WIDTH, TILE_HEIGHT), tile_map[row][col])
            for row in range(rows) for col in range(columns) if tile_map[row][col] != 3]  # Exclude empty tiles from generation

# Paddle class
class Paddle: ##################################### adjust paddle size with modifiers
    def __init__(self, x, y, width=100, height=10, color=(0, 0, 255)):
        self.rect = pygame.Rect(x - width // 2, y, width, height)
        self.color = color
        self.magnetic = False  # Magnetic state initially off

    def enable_magnetic(self):
        """Enable magnetic state to hold the ball."""
        self.magnetic = True

    def release_magnetic(self):
        """Release magnetic state, allowing the ball to move freely."""
        self.magnetic = False

    def move(self, x, screen_width):
        """Move the paddle based on the mouse x-coordinate, constrained within screen bounds."""
        self.rect.centerx = x
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_width))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def reset_position(self, x, y):
        self.rect.centerx = x
        self.rect.y = y
        self.enable_magnetic()  # Reset to magnetic at start of level or life loss


# Ball class
class Ball: #################################### adjust ball speed with modifiers
    def __init__(self, x, y, size=10, speed=5, color=(255, 255, 255), sharp=False):
        self.rect = pygame.Rect(x, y, size, size)
        self.dx = speed
        self.dy = -speed
        self.color = color
        self.last_tile_score = 0
        self.attached_to_paddle = True  # Start attached to paddle due to magnetic property
        self.sharp = sharp  # Ball starts without sharp property

    def move(self, screen_width, screen_height, margin, score_padding, paddle):
        if self.attached_to_paddle:
            self.rect.centerx = paddle.rect.centerx
            self.rect.bottom = paddle.rect.top - 1
        else:
            self.rect.x += self.dx
            self.rect.y += self.dy

            # Bounce on screen borders
            if self.rect.left <= margin or self.rect.right >= screen_width - margin:
                self.dx = -self.dx ####################### account for stuck ball case   | <-- O --------> | (add very small gravity)
            if self.rect.top <= score_padding + margin:
                self.dy = -self.dy
            if self.rect.colliderect(paddle.rect):
                self.dy = -self.dy ####################### adjust mechanics (guide ball reflection using distance of collision from paddle center)

    def check_collision_with_tiles(self, tiles, tile_types, columns, rows):
        tiles_to_remove = set()  # Use a set to track tiles for removal after collision checks

        for i, (tile, tile_type) in enumerate(tiles):
            if self.rect.colliderect(tile):
                if tile_type == 2:  # Unbreakable tile, only reflects the ball
                    self.last_tile_score = 0
                    self.dy = -self.dy
                    return False
                elif tile_type == 1:  # Explosive tile
                    apply_explosion_effect(i, tiles, columns, rows, tiles_to_remove)
                    tiles_to_remove.add(i)  # Add explosive tile itself for removal
                    if not self.sharp:  # Only reflect the ball if it's not sharp
                        self.dy = -self.dy
                    break  # Break after handling the explosive tile collision
                elif tile_type == 4:  # Steel, turns into basic tile
                    tiles[i] = (tile, 0)  # Change steel tile to basic tile
                    self.last_tile_score = tile_types[4]["score"]
                    return True
                else:
                    # Basic destructible tiles
                    self.last_tile_score = tile_types[tile_type]["score"]
                    tiles_to_remove.add(i)
                    self.dy = -self.dy  # Reflect the ball on collision
                    break  # Exit after handling one collision

        # Remove marked tiles after all collision checks
        for index in sorted(tiles_to_remove, reverse=True):
            try:
                del tiles[index]
            except IndexError:
                print("IndexError: Attempted to delete a tile that doesn’t exist.")
        return bool(tiles_to_remove)  # Return True if any tiles were removed

    def bottom_out_of_bounds(self, screen_height, margin):
        return self.rect.bottom >= screen_height - margin

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def reset_position(self, x, y):
        self.rect.center = (x, y)
        self.attached_to_paddle = True  # Reattach to paddle on reset

    def release_from_paddle(self):
        self.attached_to_paddle = False
