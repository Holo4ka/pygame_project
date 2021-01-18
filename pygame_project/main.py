import pygame
import os
import sys

FPS = 50
SIZE = WIDTH, HEIGHT = 510, 390

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.init()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as mes:
        print("Can't load image: ", mes)
        raise SystemExit(mes)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    ball, output_x, output_y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == 'x':
                Tile('gates', x, y)
            elif level[y][x] == '@':
                Tile('grass', x, y)
                ball = Ball(x, y)
                output_x, output_y = x, y
    return ball, output_x, output_y


def rules_screen():
    pass


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 302 <= event.pos[0] <= 421 and 287 <= event.pos[1] <= 325:
                    return
                elif 302 <= event.pos[0] <= 421 and 336 <= event.pos[1] <= 374:
                    rules_screen()
        pygame.display.flip()
        clock.tick(FPS)


def whose_turn(is_player_1):
    font = pygame.font.Font(None, 30)
    if is_player_1:
        turn = font.render('Ход игрока 1', True, pygame.Color('yellow'))
    else:
        turn = font.render('Ход игрока 2', True, pygame.Color('yellow'))
    turn_x, turn_y = tile_width * 12, tile_width * 8
    screen.blit(turn, (turn_x, turn_y))


class Field:
    def __init__(self, width, height, x, y, x0=0, y0=30, cell_size=30, color=(255, 255, 255)):
        self.field = [[0] * width for _ in range(height)]
        self.width, self.height = width, height
        self.left = x0
        self.top = y0
        self.cell_size = cell_size
        self.color = color
        self.field[5][5] = 1

    def set_view(self, x0, y0, cell_size, color=(255, 255, 255)):
        self.left = x0
        self.top = y0
        self.cell_size = cell_size
        self.color = color

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                color = (255, 255, 255)
                if self.field[j][i]:
                    Cross(i, j + 1)
                pygame.draw.rect(screen, color, ((i * self.cell_size + self.left, j * self.cell_size + self.top),
                                                      (self.cell_size, self.cell_size)), 1)

    def get_cell(self, x, y):
        if self.in_field(x, y):
            x -= self.left
            x = x // self.cell_size
            y -= self.top
            y = y // self.cell_size
            return x, y
        return None

    def in_field(self, x, y):
        if x < self.left or y < self.top or x > self.left + self.width * self.cell_size or \
                                y > self.top + self.height * self.cell_size:
            return False
        return True

    def get_x(self, x):
        x -= self.left
        x = x // self.cell_size
        return x

    def on_click(self, coord):
        i, j = coord
        self.field[j][i] = 1

    def clear(self):
        for i in range(self.width):
            for j in range(self.height):
                self.field[j][i] = 0
        for sprite in holoball_group:
            holoball_group.remove(sprite)
        for sprite in cross_group:
            cross_group.remove(sprite)


class Tile(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__(tiles, all_sprites)
        self.image = tile_images[type]
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(ball_group, all_sprites)
        self.default_pos = self.default_x, self.default_y = x, y
        self.image = ball_image
        self.rect = self.image.get_rect().move(
            tile_width * x + 1.5, tile_height * y + 1.5)
        self.pos = x, y

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * x + 1.5, tile_height * y + 1.5)


class HoloBall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(holoball_group, all_sprites)
        self.image = holoball_image
        self.rect = self.image.get_rect().move(
            tile_width * x + 1.5, tile_height * y + 1.5)
        self.pos = x, y

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * x + 1.5, tile_height * y + 1.5)


class Score(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(tiles, all_sprites)
        self.image = score_image
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)

    def update(self, player_1, player_2):
        font = pygame.font.Font(None, 60)
        score_1 = font.render(str(player_1), True, pygame.Color('yellow'))
        score_2 = font.render(str(player_2), True, pygame.Color('yellow'))
        x_1, y_1 = self.rect.x + 18, self.rect.y + 13
        x_2, y_2 = self.rect.x + 78, self.rect.y + 13
        screen.blit(score_1, (x_1, y_1))
        screen.blit(score_2, (x_2, y_2))


class ToMainMenu(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(tiles, all_sprites)
        self.image = main_menu_image
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


class Cross(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(cross_group, all_sprites)
        self.image = tile_images['cross']
        self.x = x
        self.y = y
        self.rect = self.image.get_rect().move(
            tile_width * x + 1.5, tile_height * y + 1.5)


tile_width = tile_height = 30
tile_images = {
    'grass': load_image('grass.png', -1),
    'gates': load_image('gates.png', -1),
    'cross': load_image('cross.png', -1)
}
ball_image = load_image('ball.png', -1)
holoball_image = load_image('holoball.png', -1)
score_image = load_image('score.png', -1)
main_menu_image = load_image('to_main_menu.png', -1)
all_sprites = pygame.sprite.Group()
tiles = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
holoball_group = pygame.sprite.Group()
cross_group = pygame.sprite.Group()


def check(x_0, y_0, x, y):
    y += 1
    return x_0 - 1 <= x <= x_0 + 1 and y_0 - 1 <= y <= y_0 + 1


if __name__ == '__main__':
    start_screen()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SIZE)
    running = True
    level_map = load_level('field.txt')
    ball, ball_x, ball_y = generate_level(load_level('field.txt'))
    field = Field(11, 11, ball_x, ball_y)
    score = Score(12, 4)
    to_main_menu_btn = ToMainMenu(12, 1)
    x0, y0 = ball.default_pos
    goal = False
    goal_confirmed = False
    player_1_turn = True
    coords = []
    count = 0
    moving = True
    player_1, player_2 = 0, 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not field.in_field(*event.pos):
                    x, y = event.pos
                    upper_gates = 91 <= x <= 240 and 0 <= y <= 30
                    lower_gates = 91 <= x <= 240 and 361 <= y <= 390
                    if upper_gates and count < 3:
                        x = field.get_x(x)
                        HoloBall(x, 0)
                        count = 4
                        goal = True
                    elif lower_gates and count < 3:
                        x = field.get_x(x)
                        HoloBall(x, 12)
                        count = 4
                        goal = True
                    else:
                        if 360 <= x <= 480 and 30 <= y <= 90:
                            x0, y0 = ball.default_pos
                            ball.move(x0, y0)
                            goal = False
                            goal_confirmed = False
                            player_1_turn = True
                            coords = []
                            count = 0
                            moving = True
                            player_1, player_2 = 0, 0
                            field.clear()
                            start_screen()
                else:
                    x, y = field.get_cell(*event.pos)
                    if (x, y) not in coords:
                        moving = True
                        movement_avaliable = check(x0, y0, x, y) and count < 3
                        if movement_avaliable:
                            HoloBall(x, y + 1)
                            x0, y0 = x, y + 1
                            coords.append((x, y))
                            count += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    x1, y1 = coords[-1]
                    if x0 != x1 or y0 != y1:
                        moving = False
                        if player_1_turn:
                            player_1_turn = False
                        else:
                            player_1_turn = True
                        count = 0
                    if goal:
                        goal_confirmed = True
        draw_lines(coords)
        screen.fill((0, 0, 0))
        tiles.draw(screen)
        if moving:
            holoball_group.draw(screen)
        else:
            if coords:
                x, y = coords[-1]
                ball.move(x, y + 1)
                for coord in coords:
                    field.on_click(coord)
                # coords.clear()
                for sprite in holoball_group:
                    holoball_group.remove(sprite)
        if goal_confirmed:
            if player_1_turn:
                player_1 += 1
            else:
                player_2 += 1
            field.clear()
            ball.move(ball.default_x, ball.default_y)
            coords.clear()
            count = 0
            x0, y0 = ball.default_x, ball.default_y
            field.field[5][5] = 1
            goal, goal_confirmed = False, False
        whose_turn(player_1_turn)
        cross_group.draw(screen)
        ball_group.draw(screen)
        score.update(player_1, player_2)
        clock.tick(FPS)
        field.render(screen)
        pygame.display.flip()
    pygame.quit()
