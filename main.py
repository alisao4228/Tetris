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

def create_mesh(column_max, row_max, dx, dy):
    mesh = []
    for i in range(column_max):
        mesh.append([])
        for j in range(row_max):
            mesh[i].append([1, pygame.Rect(i * dx, j * dy, dx, dy), pygame.Color("Gray")])
    return mesh


def create_tetraminos(dx, dy, column_max):
    tetraminos = [
        [[-2, 0], [-1, 0], [0, 0], [1, 0]],
        [[-1, 1], [-1, 0], [0, 0], [1, 0]],
        [[1, 1], [-1, 0], [0, 0], [1, 0]],
        [[-1, 1], [0, 1], [0, 0], [-1, 0]],
        [[1, 0], [1, 1], [0, 0], [-1, 0]],
        [[0, 1], [-1, 0], [0, 0], [1, 0]],
        [[-1, 1], [0, 1], [0, 0], [1, 0]],
    ]

    tet = [[], [], [], [], [], [], []]
    for i in range(len(tetraminos)):
        for j in range(4):
            tet[i].append( pygame.Rect(tetraminos[i][j][0] * dx + dx * (column_max // 2), tetraminos[i][j][1] * dy, dx, dy))

    return tet


def draw_mesh(screen, mesh, column_max, row_max):
    for i in range(column_max - 1):
        for j in range(row_max):
            pygame.draw.rect(screen, mesh[i][j][2], mesh[i][j][1], mesh[i][j][0])


def draw_tetramino(screen, tetramino, tet_choice):
    for i in range(4):
        tetramino.x = tet_choice[i].x
        tetramino.y = tet_choice[i].y
        pygame.draw.rect(screen, pygame.Color("White"), tetramino)


def draw_next_tetramino(screen, next_tetramino, next_choice, dx, dy):
    for i in range(4):
        next_tetramino.x = next_choice[i].x + dx * 8
        next_tetramino.y = next_choice[i].y + dy * 7
        pygame.draw.rect(screen, pygame.Color("White"), next_tetramino)

