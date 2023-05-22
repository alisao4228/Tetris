import pygame, random, copy


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

def draw_text(screen, font, text, x, y):
    text_surface = font.render(text,True, pygame.Color("White"))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def load_leaderboard():
    leaderboard = {}
    try:
        with open("leaderboard.txt", "r") as file:
            for line in file:
                name, score = line.strip().split(",")
                score = int(score)
                if name in leaderboard:
                    if score > leaderboard[name]:
                        leaderboard[name] = score
                else:
                    leaderboard[name] = score
    except FileNotFoundError:
        pass
    return leaderboard

def save_leaderboard(leaderboard):
    with open("leaderboard.txt", "w") as file:
        for name, score in leaderboard.items():
            file.write(f"{name},{score}\n")

def game_over(screen, score, screen_x, screen_y, player_name):
    screen.fill(pygame.Color("Black"))

    gameover_font = pygame.font.Font(None, 40)
    gameover_text = gameover_font.render("Game Over", True, pygame.Color("White"))
    score_text = gameover_font.render(f"Score: {score}", True, pygame.Color("White"))
    gameover_rect = gameover_text.get_rect()
    score_rect = score_text.get_rect()
    gameover_rect.center = (screen_x // 2 + 100, screen_y // 2 - 250)
    score_rect.center = (screen_x // 2 + 100, screen_y // 2 - 190)
    screen.blit(gameover_text, gameover_rect)
    screen.blit(score_text, score_rect)

    leaderboard = load_leaderboard()
    if player_name in leaderboard:

        if score > leaderboard[player_name]:
            leaderboard[player_name] = score
    else:
        leaderboard[player_name] = score

    save_leaderboard(leaderboard)

    leaderboard_font = pygame.font.Font(None, 40)
    leaderboard_x = screen_x // 2
    leaderboard_y = screen_y // 2 - 40
    leaderboard_spacing = 40

    leaderboard_title = leaderboard_font.render("Leaderboard:", True, pygame.Color("White"))
    leaderboard_title_rect = leaderboard_title.get_rect()
    leaderboard_title_rect.topleft = (leaderboard_x, leaderboard_y - 50)
    screen.blit(leaderboard_title, leaderboard_title_rect)

    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    for i, (name, score) in enumerate(sorted_leaderboard[:5]):
        player_rank = i + 1
        leaderboard_entry = f"{player_rank}. {name}: {score}"
        leaderboard_entry_text = leaderboard_font.render(leaderboard_entry, True, pygame.Color("White"))
        leaderboard_entry_rect = leaderboard_entry_text.get_rect()
        leaderboard_entry_rect.topleft = (leaderboard_x, leaderboard_y + i * leaderboard_spacing)
        screen.blit(leaderboard_entry_text, leaderboard_entry_rect)

    pygame.display.flip()
    pygame.time.wait(10000)

    pygame.display.quit()



def run_game():
    player_name = input("Enter your name: ")
    column_max, row_max, screen_x, screen_y, fps, score_area_width, screen, clock, tetramino, next_tetramino, dx,dy = initialize_game()

    mesh = create_mesh(column_max, row_max, dx, dy)
    tet = create_tetraminos(dx, dy, column_max)
    tet_choice = copy.deepcopy(random.choice(tet))
    next_choice = copy.deepcopy(random.choice(tet))

    count = 0
    score = 0
    level = 1
    lines_cleared = 0
    game = True
    rotate = False

    while game:
        del_x = 0
        del_y = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    del_x = -1
                elif event.key == pygame.K_RIGHT:
                    del_x = 1
                elif event.key == pygame.K_UP:
                    rotate = True

        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            count = 31 * fps

        screen.fill(pygame.Color("Black"))

        draw_mesh(screen, mesh, column_max, row_max)

        # границы
        for i in range(4):
            if ((tet_choice[i].x + del_x * dx < 0) or (tet_choice[i].x + del_x * dx >= screen_x)):
                del_x = 0

            if ((tet_choice[i].y + dy >= screen_y) or (mesh[int(tet_choice[i].x // dx)][int(tet_choice[i].y // dy) + 1][0] == 0)):
                del_y = 0

                for i in range(4):
                    x = int(tet_choice[i].x // dx)
                    y = int(tet_choice[i].y // dy)

                    mesh[x][y][0] = 0
                    mesh[x][y][2] = pygame.Color("White")

                tetramino.x = 0
                tetramino.y = 0

                tet_choice = next_choice
                next_choice = copy.deepcopy(random.choice(tet))

        for i in range(4):
            if (
                    mesh[int(tet_choice[i].x // dx)][int(tet_choice[i].y // dy) + 1][0] == 0
                    and tet_choice[i].y - dy < screen_y
            ):
                game = False

        # передвижение по x
        for i in range(4):
            tet_choice[i].x += del_x * dx

        count += fps
        # передвижение по y
        if count > 30 * fps: # чтобы двигалось каждые 30 обновлений
            for i in range(4):
                tet_choice[i].y += del_y * dy
            count = 0

        draw_tetramino(screen, tetramino, tet_choice)

        draw_next_tetramino(screen, next_tetramino, next_choice, dx, dy)

        # поворот фигуры
        if rotate:
            C = tet_choice[2]
            tet_choice = [pygame.math.Vector2(C.x - (t.y - C.y), C.y + (t.x - C.x)) for t in tet_choice]
            rotate = False

        # удаление заполненных строк и начисление баллов и уровня
        for j in range(row_max - 1, -1, -1):
            if all(mesh[i][j][0] == 0 for i in range(column_max - 1)):
                for l in range(column_max - 1):
                    mesh[l][0][0] = 1
                for k in range(j, -1, -1):
                    for l in range(column_max - 1):
                        mesh[l][k][0] = mesh[l][k - 1][0]
                lines_cleared += 1
                score += 100 * level

                if lines_cleared % 4 == 0:
                    level += 1
                    fps += 5

        # добавляем текст о счёте, уровне, следующей фигуре
        font = pygame.font.Font(None, 30)
        draw_text(screen, font, f"Score: {score}", 2 * screen_x // 3 + 130, 20)
        draw_text(screen, font, f"Level: {level}", 2 * screen_x // 3 + 130, 60)
        draw_text(screen, font, f"Lines: {lines_cleared}", 2 * screen_x // 3 + 130, 100)
        draw_text(screen, font, "Next:", 2 * screen_x // 3 + 130, 160)

        pygame.display.flip()
        clock.tick(fps)

    if game == False:
        game_over(screen, score, screen_x, screen_y, player_name)

run_game()

