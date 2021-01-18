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


class Field:
    def __init__(self, width, height, x, y, x0=0, y0=30, cell_size=30, color=(255, 255, 255)):
        self.field = [[0] * width for _ in range(height)]
        self.field[y][x] = 1
        self.width, self.height = width, height
        self.left = x0
        self.top = y0
        self.cell_size = cell_size
        self.color = color

    def set_view(self, x0, y0, cell_size, color=(255, 255, 255)):
        self.left = x0
        self.top = y0
        self.cell_size = cell_size
        self.color = color

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, self.color, ((i * self.cell_size + self.left, j * self.cell_size + self.top),
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

    def on_click(self, mousepos):
        i, j = self.get_cell(*mousepos)
        self.field[j][i] = 1


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
            tile_width * x, tile_height * y)
        self.pos = x, y

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * x + 1.5, tile_height * y + 1.5)


class HoloBall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(holoball_group, all_sprites)
        self.image = holoball_image
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.pos = x, y

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * x + 1.5, tile_height * y + 1.5)


class Score(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(tiles, all_sprites)
        self.image = score_image
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


class ToMainMenu(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(tiles, all_sprites)
        self.image = main_menu_image
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


tile_width = tile_height = 30
tile_images = {
    'grass': load_image('grass.png', -1),
    'gates': load_image('gates.png', -1)
}
ball_image = load_image('ball.png', -1)
holoball_image = load_image('holoball.png', -1)
score_image = load_image('score.png', -1)
main_menu_image = load_image('to_main_menu.png', -1)
all_sprites = pygame.sprite.Group()
tiles = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
holoball_group = pygame.sprite.Group()


def check(x_0, y_0, x, y):
    y += 1
    return x_0 - 1 <= x <= x_0 + 1 and y_0 - 1 <= y <= y_0 + 1


def move_hero(field, ball, movement):
    x, y = ball.pos
    dy, dx = movement
    if abs(dx - x) in (0, 1) and abs(dy - y) in (0, 1) and 0 <= dx <= field.width + 1 and 0 <= dy <= field.height + 1:
        if level_map[dy][dx] in '@.':
            ball.move(dx, dy)
        elif level_map[dy][dx] == 'x':
            ball.move(*ball.default_pos)


if __name__ == '__main__':
    start_screen()
    running = True
    level_map = load_level('field.txt')
    ball, ball_x, ball_y = generate_level(level_map)
    field = Field(11, 11, ball_x, ball_y)
    score = Score(12, 4)
    to_main_menu = ToMainMenu(12, 1)
    is_player_1 = True
    player_1, player_2 = 0, 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print(player_1, player_2)
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            #         # player.rect.x -= tile_width
            #         move_hero(ball, 'left')
            #     elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            #         # player.rect.x += tile_width
            #         move_hero(ball, 'right')
            #     if event.key == pygame.K_UP or event.key == pygame.K_w:
            #         # player.rect.y -= tile_height
            #         move_hero(ball, 'up')
            #     elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            #         # player.rect.y += tile_height
            #         move_hero(ball, 'down')
            if event.type == pygame.MOUSEBUTTONDOWN:
                move_hero(field, ball, (event.pos[1] // tile_height,
                                        event.pos[0] // tile_width))
        screen.fill((0, 0, 0))
        tiles.draw(screen)
        ball_group.draw(screen)
        clock.tick(FPS)
        field.render(screen)
        pygame.display.flip()
    pygame.quit()
