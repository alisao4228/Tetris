import pygame


def initialize_game():
    pygame.init()

    column_max = 11
    row_max = 21
    screen_x = 300
    screen_y = 600
    fps = 30
    score_area_width = 200
    dx = screen_x / (column_max - 1)
    dy = screen_y / (row_max - 1)

    tetramino = pygame.Rect(0, 0, dx, dy)
    next_tetramino = pygame.Rect(0, 0, dx, dy)

    screen = pygame.display.set_mode((screen_x + score_area_width, screen_y))
    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock()

    return column_max, row_max, screen_x, screen_y, fps, score_area_width, screen, clock, tetramino, next_tetramino, dx, dy
