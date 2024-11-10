import pygame

def draw_main_menu(screen, font):
    screen.fill((0, 0, 0))
    title_text = font.render("Tile Breaker Game", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
    screen.blit(title_text, title_rect)

    start_text = font.render("Start", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    pygame.draw.rect(screen, (100, 100, 100), start_rect.inflate(20, 10))
    screen.blit(start_text, start_rect)

    highscore_text = font.render("Highscore", True, (255, 255, 255))
    highscore_rect = highscore_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
    pygame.draw.rect(screen, (100, 100, 100), highscore_rect.inflate(20, 10))
    screen.blit(highscore_text, highscore_rect)

    return start_rect, highscore_rect


def draw_highscore_screen(screen, font, highscores):
    screen.fill((0, 0, 0))
    title_text = font.render("Highscores", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 8))
    screen.blit(title_text, title_rect)

    for i, entry in enumerate(highscores[:10]):
        score_text = font.render(f"{i + 1}. {entry['name']} - {entry['score']}", True, (255, 255, 255))
        screen.blit(score_text, (screen.get_width() // 2 - 100, screen.get_height() // 8 + 50 + i * 30))

    reset_text = font.render("Reset", True, (255, 255, 255))
    reset_rect = reset_text.get_rect(center=(screen.get_width() // 2 - 100, screen.get_height() - 50))
    pygame.draw.rect(screen, (100, 100, 100), reset_rect.inflate(20, 10))
    screen.blit(reset_text, reset_rect)

    back_text = font.render("Back", True, (255, 255, 255))
    back_rect = back_text.get_rect(center=(screen.get_width() // 2 + 100, screen.get_height() - 50))
    pygame.draw.rect(screen, (100, 100, 100), back_rect.inflate(20, 10))
    screen.blit(back_text, back_rect)

    return reset_rect, back_rect


def draw_score_and_lives(screen, font, score, lives, screen_width, margin):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (margin, margin // 2))

    life_display_size = 20
    for i in range(lives):
        life_rect = pygame.Rect(screen_width - margin - (i + 1) * (life_display_size + 5), margin, life_display_size, life_display_size // 2)
        pygame.draw.rect(screen, (0, 0, 255), life_rect)
